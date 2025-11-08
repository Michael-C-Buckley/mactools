{self, ...}: {
  perSystem = {pkgs, ...}: let
    pyproject = builtins.fromTOML (builtins.readFile "${self}/pyproject.toml");
    inherit (pyproject.project) name version description;
  in {
    packages.default = pkgs.python3Packages.buildPythonPackage {
      pname = name;
      version = version;
      src = self;

      format = "pyproject";

      nativeBuildInputs = with pkgs.python3Packages; [
        setuptools
      ];

      doCheck = true;

      checkPhase = ''
        python -m unittest discover tests/ -v
      '';

      pythonImportsCheck = ["mactools"];

      meta = with pkgs.lib; {
        description = description;
        license = licenses.mit;
        maintainers = [];
      };
    };
  };
}
