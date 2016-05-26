# Sort JavaScript Imports

Sublime Text package adding a new Sort command which sorts selected lines comtaining JavaScript `import` statements or `require()` calls by the modules they're importing.

## Install via [Package Control](https://packagecontrol.io/)

`Ctrl+Shift+P`/`Command+Shift+P` → Package Control: Install Package → Sort JavaScript Imports

## Install via `git clone`

Preferences → Browse Packages… → `git clone https://github.com/insin/sublime-sort-javascript-imports.git "Sort JavaScript Imports"`

## Usage

Select lines containing the import statements you want to sort, then either:

- `Ctrl+Shift+P` → Sort JavaScript Imports, or
- `Alt+F9` on Linux/Windows or `Alt+F5` on Mac (by default)

Lines will be sorted based on the module being imported, respecting (and normalising) any blank lines used to split the imports into different sections.

## Import ordering

Where top-level imports and path-based imports are mixed in the same block, they will be ordered as follows:

1. Top-level imports
2. Imports which traverse up out of the current directory, from furthest away to closest
3. Imports within the current directory

**Note:** if you're using Webpack aliases or a Babel alises plugin for top-level importing of your app's own code, you might want to put those in a separate block for clarity.

## Example

![](example.gif)

## MIT Licensed

Unit testing and configuration setup cribbed from [Sort Lines (Numerically)](https://github.com/alimony/sublime-sort-numerically).
