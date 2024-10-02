use std::env;
use std::fs::File;
use std::io;
use std::io::BufRead;

fn main() {
    if let Some(filename) = env::args().nth(1) { 
        match File::open(&filename) { 
            Ok(file) => { 
                let diagnostics = load_diagnostics(io::BufReader::new(file)); 
                let life_support = check_life_support(diagnostics); 
                println!("Life Support rate: {}", life_support); 
            }
            Err(error) => eprintln!("Cannot open file: {}", error) 
        }
    }
    else{ 
        eprintln!("Can't execute program, please run like this and make sure the file is in the same folder: csci4342_HW2.rs <filename>.txt")
    }
}
//create a function with a generic type that implements BufRead and a reader parameter, which returns a vector of vectors of characters                                                              
//this is a generic type that we specified to implement BufRead, so that we can use BufRead specific methods from the trait like .lines()
//just the reader parameter is not enough because rust binds this part at compile time
fn load_diagnostics<E: BufRead>(reader: E) -> Vec<Vec<char>> {
    println!("Loading diagnostics...");
    let mut binary_strings = Vec::new();  //create a new mutable vector 
    for line in reader.lines() { //loop through every line in the file
        if let Ok(line) = line { //if we successfully iterate, move on
            let line = line.trim().to_string(); //trim the line's whitespace
            if !line.is_empty() { //ensure the string isn't empty
                binary_strings.push(line); //push the line onto the vector
            }
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

fn check_life_support (vec_of_binary_str: Vec<Vec<char>>) -> i32 { //defines a function which takes vector of vectors as a param and returns a int 
    let mut o2_scrubber = String::new();
    let mut co2_scrubber = String::new();
    let mut remaining_o2 = vec_of_binary_str.clone();
    let mut remaining_co2 = vec_of_binary_str.clone();
    
    for i in 0..vec_of_binary_str.len() {
        if remaining_o2.len() > 1 {
            let count_0 = remaining_o2[i].iter().filter(|&&c| c == '0').count();
            let count_1 = remaining_o2[i].iter().filter(|&&c| c == '1').count();
            let most_common = if count_0 > count_1 { '0' } else { '1' };
            remaining_o2.retain(|x| x[i] == most_common);
        }
        
        if remaining_co2.len() > 1 {
            let count_0 = remaining_co2[i].iter().filter(|&&c| c == '0').count();
            let count_1 = remaining_co2[i].iter().filter(|&&c| c == '1').count();
            let least_common = if count_0 <= count_1 { '0' } else { '1' };
            remaining_co2.retain(|x| x[i] == least_common);
        }
    }
    
    for i in 0..vec_of_binary_str.len() {
        o2_scrubber.push(remaining_o2[0][i]);
        co2_scrubber.push(remaining_co2[0][i]);
    }
    
    println!("O2 Generator computed...");
    println!("CO2 Scrubber rate computed...");
    let o2_scrubber_int = i32::from_str_radix(&o2_scrubber, 2).unwrap(); 
    let co2_scrubber_int = i32::from_str_radix(&co2_scrubber, 2).unwrap();// 
    return o2_scrubber_int * co2_scrubber_int
}