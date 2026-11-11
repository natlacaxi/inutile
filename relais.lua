local l = io.read("l")
local v, t = l:match("^(.-)\t(.*)$")
print(v .. "\t" .. t .. ">Lua")
