use std::env;
use std::fs::File;
use std::io;
use std::io::BufRead;

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
        eprintln!("Can't execute program, please run like this and make sure the file is in the same folder: csci4342_HW2.rs <filename>.txt")
    }
}
//create a function with a generic type that implements BufRead and a reader parameter, which returns a vector of vectors of characters                                                              
//this is a generic type that we specified to implement BufRead, so that we can use BufRead specific methods from the trait like .lines()
//just the reader parameter is not enough because rust binds this part at compile time
fn load_diagnostics<E: BufRead>(reader: E) -> Vec<Vec<char>> {
    println!("Loading diagnostics...");
    let mut binary_strings = Vec::new(); //derive the max length of the set of strings by looking at the first
    for line in reader.lines() { //loop through each line in the file
        if let Ok(line) = line { //try to process line, move on only if successful
            let line = line.trim().to_string(); //trim whitespace
            if !line.is_empty() { //ensure string isn't empty first
                binary_strings.push(line.chars().collect()); //push the line onto the binary_strings vector as a vector of char
            }
        }
    }
    return binary_strings;
}

fn check_life_support(vec_of_binary_str: Vec<Vec<char>>) -> i32 {
    let mut o2_scrubber = vec_of_binary_str.clone(); //create clones to modify seperately
    let mut co2_scrubber = vec_of_binary_str.clone();

    for i in 0..vec_of_binary_str[0].len() { //loop through each position
        if o2_scrubber.len() > 1 { //if there is at least two strings left
            let count_0 = o2_scrubber.iter().filter(|x| x[i] == '0').count(); //count the # of vectors with 0 at index i
            let count_1 = o2_scrubber.iter().filter(|x| x[i] == '1').count(); //count the # of vectors with 1 at index i
            let most_common = if count_1 >= count_0 { '1' } else { '0' }; //add most common bit to our reference string
            o2_scrubber.retain(|x| x[i] == most_common); //remove all the strings that do not match the most common value at index i
        }

        if co2_scrubber.len() > 1 { //same thing as above but inverted
            let count_0 = co2_scrubber.iter().filter(|x| x[i] == '0').count();
            let count_1 = co2_scrubber.iter().filter(|x| x[i] == '1').count();
            let least_common = if count_0 <= count_1 { '0' } else { '1' };
            co2_scrubber.retain(|x| x[i] == least_common);
        }
    }

    let o2_scrubber_str: String = o2_scrubber[0].iter().collect(); //convert the remaining vectors into strings
    let co2_scrubber_str: String = co2_scrubber[0].iter().collect();

    println!("O2 Generator computed...");
    println!("CO2 Scrubber rate computed...");

    let o2_scrubber_int = i32::from_str_radix(&o2_scrubber_str, 2).unwrap(); //and then convert them to int values
    let co2_scrubber_int = i32::from_str_radix(&co2_scrubber_str, 2).unwrap();

    return o2_scrubber_int * co2_scrubber_int;
}