## Quick Start

### Example Runs

#### The entire CIM with a schema file for each package

```shell
$ cim2linkml data/cim.qea
```

#### The entire CIM as a single schema

```shell
$ cim2linkml data/cim.qea --single-schema
```

#### A schema for a specific package, e.g. the Core package from IEC 61970, outputted to a specified directory

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970.Base.Core -o /data/output/
```

#### Multiple schema files for several packages

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970.Base.Core -p schemas/TC57CIM/IEC61968/AssetInfo.yml
```

#### A single schema for several packages

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970.Base.Core \\
                              -p schemas/TC57CIM/IEC61968/AssetInfo.yml \\
                              --single-schema
```

## Roadmap

Using the `--schemas-for-subpackges` flag to recursively create schemas for subpackages of the
 specified packages as well.

#### A single schema for specified packages and all subpackages:

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970 --single-schema
```




