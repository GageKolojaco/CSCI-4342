local file = io.open("10000nums.txt", "w")

for i = 1, 10000 do
    -- Randomly generate either an integer or a decimal number
    local num
    num = math.random(1, 100000)  -- Random integer between 1 and 100000
    file:write(num .. " ")
end

file:close()