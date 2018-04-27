#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Shawn Yan'
__date__ = '10:37 2018/4/25'

##;; <1> input\case0_0\par\top.pdc
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25 PULLMODE=NA DRIVE=NA} [get_ports {in1[0]}]
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25 PULLMODE=NA DRIVE=NA} [get_ports {in1[1]}]
##;; create_clock -name {clk} -period 10 [get_ports clk]
##;; set_input_delay -clock [get_clocks clk] 10 [get_ports {in1[0]}]
##;; set_input_delay -clock [get_clocks clk] 10 [get_ports {in1[1]}]
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25}
##;; ldc_set_vcc -bank 0 2.5
##;; ldc_set_vcc -bank 1 2.5
##;; ldc_set_vcc -bank 2 2.5

##;; <1> output\case0_0\par\top.pdc
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25 DRIVE=6 PULLMODE=NA} [get_ports {out1[0]}]
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25 DRIVE=6 PULLMODE=NA} [get_ports {out1[1]}]
##;; create_clock -name {clk} -period 10 [get_ports clk]
##;; set_output_delay -clock [get_clocks clk] 10 [get_ports {out1[0]}]
##;; set_output_delay -clock [get_clocks clk] 10 [get_ports {out1[1]}]
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25}
##;; ldc_set_vcc -bank 0 2.5
##;; ldc_set_vcc -bank 1 2.5
##;; ldc_set_vcc -bank 2 2.5

##;; <1> bidi\case0_0\par\top.pdc
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25 DRIVE=6 PULLMODE=100K} [get_ports {bidi[0]}]
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25 DRIVE=6 PULLMODE=3P3K} [get_ports {bidi[1]}]
##;; create_clock -name {clk} -period 10 [get_ports clk]
##;; set_input_delay -clock [get_clocks clk] 10 [get_ports {bidi[0]}]
##;; set_input_delay -clock [get_clocks clk] 10 [get_ports {bidi[1]}]
##;; set_output_delay -clock [get_clocks clk] 10 [get_ports {bidi[0]}]
##;; set_output_delay -clock [get_clocks clk] 10 [get_ports {bidi[1]}]
##;; ldc_set_port -iobuf {IO_TYPE=LVCMOS25}
##;; ldc_set_vcc -bank 0 2.5
##;; ldc_set_vcc -bank 1 2.5
##;; ldc_set_vcc -bank 2 2.5


class GenIOBufferPDC:
    def __init__(self, combine_strings, banks, voltage, port_name, port_type, default_io_type):
        self.combine_strings = combine_strings
        self.banks = banks
        self.voltage = voltage
        self.port_name = port_name
        self.port_type = port_type
        self.default_io_type = default_io_type
        assert port_type in ("input", "output", "bidi"), "Unknown Port Type: %s" % port_type

    def _1_ldc_set_port(self):
        t = list()
        t.append("## Port Type: %s" % self.port_type)
        for i, cs in enumerate(self.combine_strings):
            t.append("ldc_set_port -iobuf {%s} [get_ports {%s[%d]}]" % (cs, self.port_name, i))
        return t

    def _2_set_xxx_delay(self):
        t = list()
        if self.port_type == "bidi":
            dl = ("input", "output")
        else:
            dl = (self.port_type, )

        for foo in dl:
            for i, cs in enumerate(self.combine_strings):
                t.append("set_%s_delay -clock [get_clocks clk] 10 [get_ports {%s[%d]}]" % (foo, self.port_name, i))
        return t

    def _3_ldc_set_vcc(self):
        t = list()
        t.append("ldc_set_port -iobuf {IO_TYPE=%s}" % self.default_io_type)
        for b in self.banks:
            t.append("ldc_set_vcc -bank %s %s" % (b, self.voltage))
        return t

    def get_pdc_lines(self):
        pdc_lines = list()
        pdc_lines.extend(self._1_ldc_set_port())
        pdc_lines.append("create_clock -name {clk} -period 10 [get_ports clk]")
        pdc_lines.extend(self._2_set_xxx_delay())
        pdc_lines.extend(self._3_ldc_set_vcc())
        return pdc_lines

    def gen_conf_lines(self):
        conf_lines = list()
        conf_lines.append(";; Port Type: %s" % self.port_type)
        conf_lines.append("[configuration information]")
        conf_lines.append("area = IO BUFFER SETTINGS")
        conf_lines.append("type = twr check")
        conf_lines.append("[method]")
        conf_lines.append("check_diamond_flow = 1")
        len_cs = len(self.combine_strings)
        if self.port_type == "bidi":
            _range = 6 * len_cs + 1
        else:
            _range = 3 * len_cs + 1
        conf_lines.extend(["check_lines_%02d = 1" % i for i in range(1, _range)])
        conf_lines.append("[check_diamond_flow]")
        conf_lines.append("check_flow = par,download")

        def _conf(twr_file, chk_stamp, xxx_delay):
            t = list()
            t.append(twr_file)
            t.append("check_1 = %s: %s" % (chk_stamp, xxx_delay))
            t.append("check_3 = 1 paths scored")
            return t

        set_delay_list = self._2_set_xxx_delay()
        _twr_file = "file = ./_scratch/impl1/top_impl1.twr"
        _chk_stamp = "Setup path details for constraint"
        _chk_stamp2 = "Hold path details for constraint"
        _tw1_file = "file = ./_scratch/impl1/top_impl1.tw1"
        _1st = [_conf(_twr_file, _chk_stamp, item) for item in set_delay_list]
        _2nd = [_conf(_tw1_file, _chk_stamp, item) for item in set_delay_list]
        _3rd = [_conf(_twr_file, _chk_stamp2, item) for item in set_delay_list]

        chk_no = 0
        for foo in (_1st, _2nd, _3rd):
            for bar in foo:
                chk_no += 1
                conf_lines.append("[check_lines_%02d]" % chk_no)
                for fei in bar:
                    conf_lines.append(fei)
        return conf_lines


if __name__ == "__main__":
    my_tst = GenIOBufferPDC(("one", "two"), ("1", "2", "3", "6", "7"), "2.5", "in1", "input", "LVCMOS25")
    for line in my_tst.get_pdc_lines():
        print line
    for j in my_tst.gen_conf_lines():
        print j
    print "===="
    my_tst = GenIOBufferPDC(("one", "two"), ("1", "2", "3", "6", "7"), "2.5", "out1", "output", "LVCMOS25")
    for line in my_tst.get_pdc_lines():
        print line
    for j in my_tst.gen_conf_lines():
        print j
    print "===="
    my_tst = GenIOBufferPDC(("one", "two"), ("1", "2", "3", "6", "7"), "2.5", "bidi", "bidi", "LVCMOS25")
    for line in my_tst.get_pdc_lines():
        print line
    print "===="

    for j in my_tst.gen_conf_lines():
        print j


