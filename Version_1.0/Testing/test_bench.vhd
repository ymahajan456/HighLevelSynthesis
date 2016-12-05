library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all ;
use ieee.std_logic_textio.all;

entity tb is
end entity;

architecture test of tb is
    component binding is
    generic(data_width : integer := 16);
    port(
        clk,reset : in std_logic;
        start : in std_logic;
        a,b,c,d : in std_logic_vector(data_width-1 downto 0);
        output_0, output_1, output_2 : out std_logic_vector(data_width-1 downto 0) := (others => '0');
        complete: out std_logic := '0');
    end component;
    
    function vec_to_str (x : std_logic_vector) return String is
		variable L : line ;
		variable W : String (1 to x'length) := (others =>'0');
	begin
		write(L,x);
		W(L.all'range) := L.all;
		Deallocate(L);
		return W ;
	end vec_to_str ;
    
    signal clk,start: std_logic := '0';
    signal rst: std_logic := '1';
    signal done: std_logic;
    --signal a_in, b_in, c_in, d_in, out0_ref, out1_ref, out2_ref : std_logic_vector(data_width-1 downto 0);
    signal a,b,c,d,out_0, out_1, out_2: std_logic_vector(15 downto 0) := (others => '0');
begin

    dut: binding
    generic map(16)
    port map(clk => clk, reset => rst,start => start, a => a, b=> b, c=>c, d=> d, output_0 => out_0, output_1 => out_1, output_2 => out_2, complete => done);
    
    process
    begin
        clk <= not clk;
        wait for 10 ns;
    end process;
    
    process
        file f: text open read_mode is "test.txt";
        variable a_in, b_in, c_in, d_in, out0_ref, out1_ref, out2_ref : std_logic_vector(15 downto 0);
        variable L: line;
        variable fail_count: integer := 0;
        variable in_count: integer := 0;
        
    begin
        rst <= '1';
        wait until (clk = '1');
        wait until (clk = '1');
        rst <= '0';
        wait until (clk = '1');
        while not endfile(f) loop
        
            readline(f,L);
            read(L,a_in);
            read(L,b_in);
            read(L,c_in);
            read(L,d_in);
            read(L,out0_ref);
            read(L,out1_ref);
            read(L,out2_ref);
            in_count := in_count + 1;
            
            report "Test Number : " & integer'image(in_count);
            
            a <= a_in;
            b <= b_in;
            c <= c_in;
            d <= d_in;
            
            wait until (clk = '1');
            start <= '1';
            wait until (clk = '1');
            wait until (clk = '1');
            start <= '0';
            
            wait until(done = '1');
            wait until(clk = '0');
            if (not ((out0_ref = out_0) and (out1_ref = out_1) and (out2_ref = out_2))) then
                fail_count := fail_count + 1;
                report "Error :: Inputs are : " & vec_to_str(a) & " " & vec_to_str(b) & " " & vec_to_str(c) & " " & vec_to_str(d);
                report "Outputs are : " & vec_to_str(out_0) & " " & vec_to_str(out_1) & " " & vec_to_str(out_2);
            end if;
        end loop;
        
        report "Test Completed with " & integer'image(fail_count) & " failures";
        wait;
        
    end process;
end architecture;        
        
        
