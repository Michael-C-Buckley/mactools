{pkgs}:
pkgs.mkShell {
  env = {
    LD_LIBRARY_PATH = with pkgs; lib.makeLibraryPath [stdenv.cc.cc];
    RUST_SRC_PATH = "${pkgs.rustPlatform.rustLibSrc}";
  };
  buildInputs = with pkgs; [
    # Python
    (python3.withPackages (p:
      with p; [
        pip
        setuptools
        wheel
        build
        twine
        unittest-xml-reporting
      ]))
    uv
    ruff
    gcc
    pkg-config
    basedpyright

    # Pre-commit
    lefthook
    typos
    bandit
  ];
  shellHook = ''
    export LOCALE_ARCHIVE="${pkgs.glibcLocales}/lib/locale/locale-archive"
    export LC_ALL="C.UTF-8"
    export UV_LINK_MODE=copy
    export UV_PROJECT_ENVIRONMENT="$VIRTUAL_ENV"
    lefthook install
  '';
}
