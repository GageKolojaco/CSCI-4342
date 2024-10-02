use std::env;
use std::fs::File;
use std:io::{self, BufRead};
use std::path::Path;

fn main() {
    if let Some(filename) = env::args().nth(1) { //if Some returns a value than we correctly parsed the second argument (intended to be the filename)
        match File::open(&filename) { //attempt to open the file
            Ok(file) => { //if we can successfully open the file do:
                let diagnostics = load_diagnostics(io::BufReader::new(file)); //create a new buffered reader object and pass it to load_diagnostics
                let power = check_power(diagnostics); //pass diagnostics to check_power to get our value
                println!("Power Consumption rate: {}", power); // print power value on a newline
            }
            Err(error) => eprintln!("Cannot open file: {}", error) //if we can't, state why
        }
    }
    else{ // if Some returns None than explain where the filename goes
        eprintln!("Can't execute program, please run like this and make sure the file is in the same folder: HW2.rs <filename>.txt")
    }
}

fn load_diagnostics<E: BufRead>(reader: E) -> Vec<Vec<char>>