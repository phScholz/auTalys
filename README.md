auTalys
=

This is a collection of useful python scripts for everyone who is interested in controlling and automizing [*Talys*](https://talys.eu) calculation. [*Talys*](https://talys.eu) is a FORTRAN code for nuclear reaction calculations. 

*auTalys*'s main idea is to change the input file format of Talys to a **.json* format and then use a **.json* array with Talys input parameters as input for *auTalys*.

---

- [auTalys](#autalys)
  - [Dependencies](#dependencies)
  - [Creating json-like Talys input files](#creating-json-like-talys-input-files)
  - [Starting automized Talys calculations](#starting-automized-talys-calculations)

---

## Dependencies
*auTalys* requires the following `python` packages
* `subprocess`
* `multiprocessing`
* `progressbar`
* `argparse`
* `json`

## Creating json-like Talys input files
Json input files can be generated using ```createTalysJson.py```.

```bash
python createTalysJson.py <A> <Z> <projectile>
```

## Starting automized Talys calculations

```bash
python auTalys.py <json> -o OutputDir -t TalysPath
```

