# Cutlist Calculator
Calculates most optimal cutlist for linear length materials such as beams/planks.

## Project summary
![Language](https://img.shields.io/badge/language-python%203.8-blue)
![GitHub release](https://img.shields.io/github/v/release/nick-van-h/cutlistcalculator)
![GitHub issues](https://img.shields.io/github/issues/nick-van-h/cutlistcalculator)
![GitHub pull requests](https://img.shields.io/github/issues-pr/nick-van-h/cutlistcalculator)
![GitHub license](https://img.shields.io/github/license/nick-van-h/cutlistcalculator)

## Problem statement and calculation
Given available plank length of 100 (@ 2.5 each) and 180 (@ 4 each), and required plank lengths of 60 (4x) and 90 (6x), what is the most economic solution to obtain required plank lengths?

Possible cuts include:
- 180 plank cut to 2x 90
- 180 plank cut to 1x 90 & 1x 60
- 180 plank cut to 3x 60
- 120 plank cut to 1x 90
- 120 plank cut to 2x 60
- And everything in between

Possible solutions include:
- 3x 180 plank cut to 2x 90 (@ 3x 4 = 12) + 2x 180 plank cut to 3x 60 & 1x 60 (@ 2x 4 = 8) -> Total price 20
- 3x 180 plank cut to 2x 90 (@ 3x 4 = 12) + 2x 120 plank cut to 2x 60 (@ 2x 2.5 = 5) -> Total price 17
- 6x 120 plank cut to 1x 90 (@ 6x 4 = 24) + 2x 120 plank cut to 2x 60 (@ 2x 2.5 = 5) -> Total price 29
- And everything in between

To calculate optimal cutlist following methods are used:
- Minimize waste: Sort list of possible cuts by smallest rest length
- Big lengths first: Sort list of possible cuts by biggest required lengths first
- Minimum price per used length: Sort list of possible cuts by cost price per unit based on actual used length

Results of these methods are compared and cheapest option is returned.

## Usage
The program reads an input JSON file with the required lengths + quantities and available base material + unit price, calculates the most cost efficient cutlist and outputs to another JSON file. 

### Input file lay-out
```Javascript
{
    "Cut loss": 3, //Set cut loss per cut, 0 for no cut loss 
    "Required Lengths": [
        //Collection of required lengths as end result
        {
            "Length": 60,
            "Qty": 4
        },
        {
            "Length": 90,
            "Qty": 6
        }
        //Append multiple collections for different lengths and quantities
    ],
    "Available base material": [
        //Collection of available base material lengths and price per piece (not price per unit)
        {
            "Length": 120,
            "Price": 2.5
        },
        {
            "Length": 180,
            "Price": 4
        }
        //Append multiple collections for different lengths and quantities
    ]
}
```
<sup>Note: Don't use comments (`//`) in original JSON file :unamused:</sup>

### Default behavior
Running the program without arguments takes the following input and output files.

Input file: `./input/input.json`

Output file: `./output/cutlist_result.json`

Default command: `py cutlist`

### Passing arguments
This program accepts following arguments:

`-h` or `--help` Displays help content

`-i <filepath>` or `--input <filepath>` Uses the specified file as input<br>
Example: `py cutlist -i 'C:/foo/bar.json'` uses file `bar.json` in folder `C:/foo/`

`-o <path>` or `--output <path>` Uses the specified folder as output<br>
Example: `py cutlist -o 'C:/foo/bar/'` outputs `cutlist_result.json` in folder `C:/foo/bar/`

### Return values
After code execution one of following results will be returned
- `Success` Code execution was succesful and output file has been created
- `Err: <explanation>` Unable to calculate cutlist, see explanation for reason e.g.
   - Input file not found
   - Input file not according format
   - Unable to calculate requirements with given input
