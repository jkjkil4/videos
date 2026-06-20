{
  description = "Python with uv package management";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (nixpkgs) lib;
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };

        # Use Python 3.13 from nixpkgs
        python = pkgs.python313;

        # common logic for mkShell
        mkPyuvShell =
          {
            extraPackages ? [ ],
            extraLibs ? [ ],
            shellHook ? "",
          }:
          pkgs.mkShell {
            packages = [ 
              pkgs.vista-fonts  # Consolas
              pkgs.uv 
              python
              # alias
              (pkgs.writeShellScriptBin "janim" ''
                exec uv run janim "$@"
              '')
              (pkgs.writeShellScriptBin "sphinx-build" ''
                exec uv run sphinx-build "$@"
              '')
              (pkgs.writeShellScriptBin "sphinx-intl" ''
                exec uv run sphinx-intl "$@"
              '')
            ] ++ extraPackages;

            env = {
              # Prevent uv from managing Python downloads
              UV_PYTHON_DOWNLOADS = "never";
              # Force uv to use nixpkgs Python interpreter
              UV_PYTHON = python.interpreter;
            } // lib.optionalAttrs pkgs.stdenv.isLinux {
              LD_LIBRARY_PATH =
                lib.makeLibraryPath (
                  pkgs.pythonManylinuxPackages.manylinux1
                  ++ extraLibs
                );
            };
            shellHook = ''
              unset PYTHONPATH
              ${shellHook}
            '';
          };

        extraPackages = with pkgs; [ ffmpeg ];

        guiExtraLibs = with pkgs; [
          zstd
          fontconfig
          libxkbcommon
          dbus
          wayland
          freetype
        ];

      in {
        devShells = rec {
          dev =
            mkPyuvShell {
              inherit extraPackages;
              extraLibs = guiExtraLibs;
              shellHook = "uv sync";
            };
          default = dev;
        };
      });
}

