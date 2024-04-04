import yaml

with open("out.yml") as f:
    out = yaml.safe_load(f)


with open("jemoeder.yml") as f:
   jemoeder = yaml.safe_load(f)

out_class_keys = set(out["classes"].keys())
out_enum_keys = set(out["enums"].keys())
jemoeder_class_keys = set(jemoeder["classes"].keys())
jemoeder_enum_keys = set(jemoeder["enums"].keys())

assert jemoeder_class_keys == out_class_keys
assert jemoeder_enum_keys == out_enum_keys

print("Different classes:")
for key in jemoeder_class_keys:
    if jemoeder["classes"][key] != out["classes"][key]:
        print(f"\t{key}")
print()

print("Different enums:")
for key in jemoeder_enum_keys:
    if jemoeder["enums"][key] != out["enums"][key]:
        print(f"\t{key}")

