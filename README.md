## Install
Make sure you have Python (≥ 3.11) and Poetry installed.

Run `poetry install` to have it set up a virtual environment for you with the necessary dependencies installed and configuration taken care of.

## Running `cim2linkml`

#### From within the virtual environment
Activate your virtual environment and you should be able to use the `cim2linkml` script.

```
$ poetry shell
$ cim2linkml --help
# ...
```

#### Using `poetry run`
You can also run the script inside the virtual environment without activating it.

```
$ poetry run cim2linkml --help
# ...
```


### Usage
```
Usage: cim2linkml [OPTIONS] QEA_FILE

  Generates LinkML schemas from the supplied Sparx EA QEA database file.

  You can specify which packages in the UML model to generate schemas from
  using the `--package` parameter, where you provide the fully qualified
  package name (e.g. TC57CIM.IEC61970.Base.Core) of each package to select it.

  If no packages are specified, the entire CIM will be selected.

  By default, a LinkML schema will be generated for each specified package.
  However, by setting the `--single-schema` flag everything is outputted to a
  single LinkML schema.

Options:
  -p, --package TEXT     Fully qualified package name. [example:
                         TC57CIM.IEC61970.Base.Core]
  -s, --single-schema    If false, a schema is generated per package.
                         Otherwise everything will be outputted to a single
                         schema.
  -o, --output-dir PATH  Directory where schemas will be outputted.  [default:
                         schemas]
  --help                 Show this message and exit.
```

### Examples

#### The entire CIM

##### Schema per package
If no package is specified, it defaults to TC57CIM, i.e. the entire CIM. For non-leaf
packages like this one, the default behavior is to generate a schema for each subpackage.

```shell
$ cim2linkml data/cim.qea
```

##### Single schema
If generating a single schema file is desired, this can be done as follows:

```shell
$ cim2linkml data/cim.qea --single-schema
```

#### Leaf package
Leaf peackages by definition don't have subpackages and therefore always become a single schema.

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970.Base.Wires
```

#### Non-leaf package

##### Including subpackages
By default, when providing a non-leaf package, all subpackages are included and schema files are
created for each package.

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970
```

If a single schema file is desired, `--single-schema` can be passed.

##### Ignoring subpackages
If only selecting the package itself is desired, i.e. not including subpackages, one can pass `--ignore-subpackages`.
Note that in this case, it is always a single schema file (`--single-schema` is implied).

```shell
$ cim2linkml data/cim.qea -p TC57CIM.IEC61970 --ignore-subpackages
```