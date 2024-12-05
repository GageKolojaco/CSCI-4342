function main()
    local start = os.clock()
    writeFile(readFile())
    local numbers = readNums()
    local sorted_nums = sort(numbers) --sorting the array makes the following functions simpler
    print("Mean: " .. mean(sorted_nums))
    print("Median: " .. median(sorted_nums))
    print("Mode: " .. mode(sorted_nums))
    print("Standard Deviation: " .. standardDeviation(sorted_nums, mean(sorted_nums)))
    local elapsed_time = os.clock() - start_time
    print("Time elapsed: " .. elapsed_time)
end

-- reading in file
function readFile()
    local input_file = io.open("input.txt", "r") -- open file for reading
    local items_read = input_file:read("*all") -- read all contents as a single string
    input_file:close() -- close the file
    return items_read
end

--writing to a file
function writeFile(input)
    local output_file = io.open("output.txt", "w")
    output_file:write(input)
    output_file:close() 
end

--reading in the number file and parsing it into a table
function readNums()
    local num_file = io.open("100000nums.txt" , "r") --open file
    local data = num_file:read("*all") --read contents into data var as one string
    local numbers = {} --init numbers table
    local num = "" --init num string
    for i = 1, #data do --loop through the data string 
        local char = data:sub(i, i) --extract the char at pos i using substring
        if char:match("%d") or (char == "." and not num:find(".")) then --check if the char is a digit or a decimal, so long as a decimal doesn't already exist in num
            num = num .. char --apend char to number if it is part of one
        else
            if #num > 0 then -- if num conatins a number
                table.insert(numbers, tonumber(num)) --insert it into the numbers table
                num = "" --reset the num string
            end
        end
    end
    if #num > 0 then --double check for unfinished num string
        table.insert(numbers, tonumber(num))
    end
    return numbers
end

--sorting the provided table using a bubble sort implementation 
function sort(numbers) 
    local table_length = #numbers --store the length of the provided table in table_length var
    for i = 1, table_length - 1 do --loop through the length of the table
        for j = 1, table_length - i do --loop through the unsorted part of the table
            if numbers[j] > numbers[j + 1] then --if the element ahead of the current one is greater
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j] --swap the positions of the elements (lua lets us do this in one line!)
            end
        end
    end
    return numbers
end

--finding the mean
function mean(numbers)
    local sum = 0
    for _ , num in next, numbers do --loop throught the table and grab the value of each entry, we don't need the key
        sum = sum + num --add it to the sum
    end
    return sum / #numbers --return the sum of the table divided by it's number of components
end

--finding the median
function median(numbers) --using a sorted table we just grab the middle component of the table
    local table_length = #numbers
    local mid = math.floor(table_length / 2)
    if table_length % 2 == 0 then
        median = (numbers[mid] + numbers[mid + 1]) / 2
    else
        median = numbers[mid + 1]
    end
    return median
end


--finding the mode
function mode(numbers) --with a sorted array we just need to iterate in a straight line down the table
    local freq = {} --init the frequency table
    for i = 1, #numbers do --loop through the length of the table
        local num = numbers[i] --store the digit at the i position in the num var
        freq[num] = (freq[num] or 0) + 1 --checks the value associated with that digit, if it doesn't exists 0 is used in its place, then add 1 to the freq of that digit
    end
    local mode, max = nil, 0 --init our mode and max vars
    for key, count in next, freq do --iterate over the freq table, storing the value of the next pair in the table in our key and count vars
        if count > max then -- if the freq of this digit is greater than our previous max freq
            mode, max = key, count --store the digit in mode and store the digit's freq in max
        end
    end
    return mode
end

--finding the standard deviation
function standardDeviation(numbers, mean)
    local deviation = 0
    for _ , num in next, numbers do
        deviation = deviation + (num - mean)^2
    end
    deviation = deviation / (#numbers - 1)
    return math.sqrt(deviation)        
end

--call the main function to begin execution
main()