LIBRARY IEEE;
USE ieee.numeric_std.all;
USE ieee.std_logic_1164.all;
USE ieee.math_real.all;

ENTITY REG IS
	GENERIC(
		data_width: INTEGER  := 0);
	PORT(
		inp: IN STD_LOGIC_VECTOR( 0 TO data_width - 1) := (others => '0');
		outp: OUT STD_LOGIC_VECTOR( 0 TO data_width - 1) := (others => '0');
		clk: IN STD_LOGIC := '0';
		clr: IN STD_LOGIC := '0';
		ena: IN STD_LOGIC := '0');
END ENTITY;

architecture myReg of REG is
begin
	process(clk,clr)
    begin
        if(clk'event and clk = '1') then
            if(ena = '1') then
                outp <= inp;
            end if;
        end if;
        if(clr = '1') then
            outp <= (others => '0');
        end if;
     end process;
end architecture;