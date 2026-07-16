{
  description = "Mactools Nix Development Shell";

  inputs.nixpkgs.url = "https://channels.nixos.org/nixos-unstable/nixexprs.tar.xz";

  outputs = {
    self,
    nixpkgs,
  }: let
    forAllSystems = nixpkgs.lib.genAttrs ["x86_64-linux" "aarch64-linux" "aarch64-darwin"];
    nixpkgsFor = forAllSystems (system: import nixpkgs {inherit system;});
  in {
    devShells = forAllSystems (
      system: {
        default = import ./nix/shell.nix {pkgs = nixpkgsFor.${system};};
      }
    );
    packages = forAllSystems (system:
      import ./nix/packages.nix {
        inherit self system;
        pkgs = nixpkgsFor.${system};
      });
  };
}
