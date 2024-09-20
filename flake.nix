{
  description = "Mactools Nix Development Shell";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };


  outputs = { self, nixpkgs }: 
  
  let
    pkgs = nixpkgs.legacyPackages.x86_64-linux.pkgs;
  in
  {

    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = with pkgs.buildPackages; [
        git
        python3
      ];
    };

  };
}
