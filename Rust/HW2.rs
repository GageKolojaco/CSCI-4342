use std::env;
use std::fs::File;
use std::io
use std::path::Path;

fn main() {
    if let Some(filename) = env::args().nth(1) { //if Some returns a value than we correctly parsed the second argument (intended to be the filename)
        match File::open(&filename) { //attempt to open the file
            Ok(file) => { //if we can successfully open the file, bind it to file variable
                let diagnostics = load_diagnostics(io::BufReader::new(file)); //create a new buffered reader object from the file and pass it to load_diagnostics
                let life_support = check_life_support(diagnostics); //pass diagnostics to check_power to get our value
                println!("Life Support rate: {}", life_support); // print life_support value on a newline
            }
            Err(error) => eprintln!("Cannot open file: {}", error) //if we can't, state why
        }
    }
    else{ // if Some returns None then explain where the filename goes
        eprintln!("Can't execute program, please run like this and make sure the file is in the same folder: HW2.rs <filename>.txt")
    }
}
//create a function with a generic type that implements BufRead and a reader parameter, which returns a vector of vectors of characters                                                              
//this is a generic type that we specified to implement BufRead, so that we can use BufRead specific methods from the trait like .lines()
//just the reader parameter is not enough because rust binds this part at compile time
fn load_diagnostics<E: BufRead>(reader: E) -> Vec<Vec<char>> {
    println!("Loading diagnostics...");
    let mut binary_strings = Vec::new(); //create a new mutable vector 
    for line in reader.lines() { //loop through every line in the file
        if let Ok(line) = line { //if we successfully iterate, move on
            let line = line.trim().to_string(); //trim the line's whitespace
            if !line.is_empty() { //ensure the string isn't empty
                binary_strings.push(line); //push the line onto the vector
            }
        }
    }
    let max_length = binary_strings[0].len(); //derive the max length of the set of strings by looking at the first
    let mut vec_of_binary_str: Vec<Vec<char>> = vec![Vec::new(); max_length]; //specify the type and then use a handy macro to create a vector of max_length vectors
    for str in binary_strings { //loop through the vector of strings
        for (index, char) in str.chars().enumerate() { //use .chars().enumerate to assign indices to each char in the given string
            vec_of_binary_str[index].push(char); //push the char to its respective vector based on its indice
        }
    }
    return vec_of_binary_str
}

fn check_life_support (vec_of_binary_str: Vec<Vec<char>>) -> i32 { //defines a function which takes vector of vectors as a param and returns a int 
    let mut o2_scrubber = String::new();
    let mut co2_scrubber = String::new();
    for binary_strings in vec_of_binary_str { //loop through the vector and count the number of 0's or 1's contained in each vector
        let count_0 = binary_strings.iter().filter(|&&c| c == '0').count();
        let count_1 = binary_strings.iter().filter(|&&c| c == '1').count();
        if count_0 > count_1 { //add one to the gamma rate for that vector only if the # of 0's is >
            o2_scrubber.push('0');
        } else {
            o2_scrubber.push('1');
        }
    }
    println!("O2 Generator computed...");
    for digit in o2_scrubber.chars() { //use a loop to flip all the values to derive the co2 scrubber rate
        if digit == '0' {
            co2_scrubber.push('1');
        } else {
            co2_scrubber.push('0');
        }
    }
    println!("CO2 Scrubber rate computed...");
    let o2_scrubber_int = i32::from_str_radix(&o2_scrubber, 2).unwrap(); //convert the string of base 2 to an int of base 10
    let co2_scrubber_int = i32::from_str_radix(&co2_scrubber, 2).unwrap();// we can use .unwrap() here to retrieve just the result without error handling, bc we are confident the value we are converting exists
    return o2_scrubber_int * co2_scrubber_int
}
    

