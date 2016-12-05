LIBRARY IEEE;
USE ieee.numeric_std.all;
USE ieee.std_logic_1164.all;
USE ieee.math_real.all;


--alu_ops_map = {
--    "+": "000",
  --  "-": "001",
--    "*": "010",
--    "/": "011",
--    "!": "100",
--    "&": "101",
 --   "^": "110",
 --   "|": "111"
 --   }

ENTITY ALU IS
	GENERIC(
		data_width: INTEGER  := 16);
	PORT(
		in_1: IN STD_LOGIC_VECTOR( 0 TO data_width - 1) := (others => '0');
		in_2: IN STD_LOGIC_VECTOR( 0 TO data_width - 1) := (others => '0');
		outp: OUT STD_LOGIC_VECTOR( 0 TO data_width - 1) := (others => '0');
		sel: IN STD_LOGIC_VECTOR( 0 TO 2 ) := (others => '0'));
END ENTITY;

architecture alu_le_le of ALU is
    signal add_out, sub_out, mul_out, div_out, not_out, and_out, xor_out, or_out: std_logic_vector(0 to data_width-1) := (others => '0');
begin
	process(in_1, in_2)
    begin
        add_out <= std_logic_vector((unsigned(in_1)) + (unsigned(in_2)));-- after 2 ns;
        --sub_out <= std_logic_vector(to_integer(unsigned(in_1)) - to_integer(unsigned(in_2)));-- after 2 ns;
        --mul_out <= std_logic_vector(to_integer(unsigned(in_1)) * to_integer(unsigned(in_2)));-- after 3 ns;
        --div_out <= std_logic_vector(to_integer(unsigned(in_1)) / to_integer(unsigned(in_2)));-- after 3 ns;
        or_out <= in_1 or in_2;-- after 1 ns;
        and_out <= in_1 and in_2;-- after 1 ns;
        not_out <= not in_1;-- after 1 ns;
        xor_out <= in_1 xor in_2;-- after 1 ns;
    end process;
    
    process(sel,add_out,sub_out,mul_out,div_out,or_out,and_out,not_out,xor_out)
    begin
        if(sel = "000") then
            outp <= add_out;
        elsif(sel = "001") then
            outp <= sub_out;
        elsif(sel = "010") then
            outp <= mul_out;
        elsif(sel = "011") then
            outp <= div_out;
        elsif(sel = "100") then
            outp <= not_out;
        elsif(sel = "101") then
            outp <= and_out;
        elsif(sel = "110") then
            outp <= xor_out;
        elsif(sel = "111") then
            outp <= or_out;
        else
            outp <= (others => '0');
        end if;
    end process;
end architecture;
