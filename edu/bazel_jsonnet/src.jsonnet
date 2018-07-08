
local x = std.extVar("x");

local dict = import "lib.libsonnet";

{
  nested: dict,
  x: x
}