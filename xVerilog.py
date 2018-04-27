#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os

__author__ = 'Shawn Yan'
__date__ = '16:00 2018/4/23'

IBIS_BASE_VERILOG = """ //IBIS Template
module top(in, out, out1, bidi, sel, clk);
input %(width_str)s in;
input sel;
input clk;

output %(width_str)s out;
output %(width_str)s out1;

reg %(width_str)s out1;
inout %(width_str)s bidi;

assign bidi = sel?in:%(width_int)d'bz;
assign out = ~in;
always@(posedge clk)
    begin
        out1 = ~bidi;
    end
endmodule
"""


IOBUFFER_BASE_VERILOG = """ //IOBUFFER Template
module top(in1, out1, bidi, sel, clk);
input %(width_str)s in1;
input sel;
input clk;
output %(width_str)s out1;
inout %(width_str)s bidi;

reg %(width_str)s in2;
reg %(width_str)s out1;

assign bidi = sel?in2:%(width_int)d'bz;

always@(posedge clk)
    begin
        in2 = ~in1;
    end
always@(posedge clk)
    begin
        out1 = ~bidi;
    end
endmodule
"""

SSO_BASE_VERILOG = """// SSO Template
`timescale 1 ns / 1 ps
module top(
input  rst_n,
input  clk,
input  %(width_str)s adc_data_i,
output %(width_str)s adc_data_o
);

reg %(width_str)s data_buf ;
always @(posedge clk or negedge rst_n)
begin
    if( !rst_n )begin
        data_buf <= %(width_int)d'h0;
    end
    else begin
        data_buf <= adc_data_i;
    end
end
assign adc_data_o = data_buf;
endmodule
"""


def _get_verilog_lines(template, width=2):
    key_words = {"width_int": width, "width_str": "[%d:0]" % (width-1)}
    return template % key_words


def get_ibis_verilog(width=16):
    return _get_verilog_lines(IBIS_BASE_VERILOG, width)


def get_iobuffer_verilog(width=32):
    return _get_verilog_lines(IOBUFFER_BASE_VERILOG, width)


def get_sso_verilog(width=64):
    return _get_verilog_lines(SSO_BASE_VERILOG, width)


if __name__ == "__main__":
    print get_ibis_verilog()
    print get_iobuffer_verilog()
    print get_sso_verilog()
