function main()
    -- ask for filename from user
    local start = os.clock
    -- numbers = processNumbers(readFile(filepath))
    -- mean(numbers) --include some formatting when we write this to the output file
    -- median(numbers)
    -- mode(numbers)
    -- standardDeviation(numbers)

-- reading in file
function readFile(filepath)
    local input_file = io.open(filepath, "r") -- open file for reading
    local data = file:read("*all") -- read all contents as a single string
    file:close() -- close the file
    return data
-- processing the numbers
function processNumbers(data)
    local numbers = {}
    for num in data:gmatch("%S+") do -- match each non-whitespace sequence
        table.insert(numbers, tonumber(num)) -- convert to number and add to the table
    end
    return numbers
local output_file = io.open("output.txt", "w") -- open file for writing
file:write("Hello, Lua!") -- write data to the file
file:close()                            -- Close the file
