{
  inputs = {
    nixpkgs.url = "github:cachix/devenv-nixpkgs/rolling";
    systems.url = "github:nix-systems/default";
    devenv.url = "github:cachix/devenv";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
    playwright.url = "github:pietdevries94/playwright-web-flake";
  };

  nixConfig = {
    extra-trusted-public-keys = "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=";
    extra-substituters = "https://devenv.cachix.org";
  };

  outputs = { self, nixpkgs, playwright, devenv, systems, ... } @ inputs:
    let
      forEachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      packages = forEachSystem (system: {
        devenv-up = self.devShells.${system}.default.config.procfileScript;
        devenv-test = self.devShells.${system}.default.config.test;
      });

      devShells = forEachSystem
        (system:
          let
            overlay = final: prev: {
              inherit (playwright.packages.${system}) playwright-test playwright-driver;
            };
            pkgs = import nixpkgs {
              inherit system;
              overlays = [ overlay ];
              config.allowUnfree = true;
            };
            buildInputs = with pkgs; [
              cudaPackages.cuda_cudart
              cudaPackages.cudatoolkit
              cudaPackages.cudnn
              stdenv.cc.cc
              libuv
              zlib
            ];
          in
          {
            default = devenv.lib.mkShell {
              inherit inputs pkgs;
              modules = [
                {
                  languages.python = {
                    enable = true;
                    uv.enable = true;
                  };

                  packages = with pkgs; [
                    playwright-test
                    cudaPackages.cuda_nvcc
                    sqlite
                  ];

                  env = {
                    PLAYWRIGHT_BROWSERS_PATH = "${pkgs.playwright-driver.browsers}";
                    PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS = "true";
                    PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD = "1";
                    LD_LIBRARY_PATH = "${
                          with pkgs;
                          lib.makeLibraryPath buildInputs
                        }:/run/opengl-driver/lib:/run/opengl-driver-32/lib";
                    XLA_FLAGS = "--xla_gpu_cuda_data_dir=${pkgs.cudaPackages.cudatoolkit}"; # For tensorflow with GPU support
                    CUDA_PATH = pkgs.cudaPackages.cudatoolkit;
                  };

                  # souce the python environment
                  enterShell = ''
                    source $DEVENV_STATE/venv/bin/activate
                  '';

                }
              ];
            };
          });
    };
}
