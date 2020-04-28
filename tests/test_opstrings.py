#!/usr/bin/python3
import gensio
import utils
from serialsim import *
import tempfile
import os

from dataxfer import test_one_xfer

print("Testing string operations")

test_one_xfer("banner", None, "Testing banner!",
              ("connection: &con",
               "  accepter: tcp,3023",
               "  connector: serialdev,/dev/ttyPipeA0,9600N81",
               "  options:",
               "    banner: \"banner1\\\\r\\\\n\""),
              "tcp,localhost,3023",
              "serialdev,/dev/ttyPipeB0,9600N81",
              compare2 = "banner1\r\nTesting banner!")

test_one_xfer("openstr", "Testing openstr!", None,
              ("connection: &con",
               "  accepter: tcp,3023",
               "  connector: serialdev,/dev/ttyPipeA0,9600N81",
               "  options:",
               "    openstr: \"str1\""),
              "tcp,localhost,3023",
              "serialdev,/dev/ttyPipeB0,9600N81",
              compare1 = "str1Testing openstr!")

test_one_xfer("openstr", "Testing openstr!", None,
              ("connection: &con",
               "  accepter: tcp,3023",
               "  connector: serialdev,/dev/ttyPipeA0,9600N81",
               "  options:",
               "    openstr: \"str1\""),
              "tcp,localhost,3023",
              "serialdev,/dev/ttyPipeB0,9600N81",
              compare1 = "str1Testing openstr!")

print("  closestr")
ser2net, io1, io2 = utils.setup_2_ser2net(utils.o,
              ("connection: &con",
               "  accepter: tcp,3023",
               "  connector: serialdev,/dev/ttyPipeA0,9600N81",
               "  options:",
               "    closestr: \"str2\""),
              "tcp,localhost,3023",
              "serialdev,/dev/ttyPipeB0,9600N81")
try:
    utils.test_dataxfer(io1, io2, "Testing closestr")
    io2.handler.set_compare("str2")
    utils.io_close(io1)
    if io2.handler.wait_timeout(1000) == 0:
        raise Exception("closestr: Timed out waiting for closestr")
finally:
    utils.finish_2_ser2net(ser2net, io1, io2)

print("  closeon")
ser2net, io1, io2 = utils.setup_2_ser2net(utils.o,
              ("connection: &con",
               "  accepter: tcp,3023",
               "  connector: serialdev,/dev/ttyPipeA0,9600N81",
               "  options:",
               "    closeon: \"str3\""),
              "tcp,localhost,3023",
              "serialdev,/dev/ttyPipeB0,9600N81")
try:
    io1.handler.set_expected_err("Remote end closed connection")
    io1.handler.set_compare("str3")
    utils.test_dataxfer(io2, io1, "str3")
    io1.read_cb_enable(True)
    if io1.handler.wait_timeout(1000) == 0:
        raise Exception("closestr: Timed out waiting for closestr")
finally:
    utils.finish_2_ser2net(ser2net, io1, io2)

print("  sendon")
ser2net, io1, io2 = utils.setup_2_ser2net(utils.o,
              ("connection: &con",
               "  accepter: tcp,3023",
               "  connector: serialdev,/dev/ttyPipeA0,9600N81",
               "  options:",
               "    chardelay-min: 5000000",
               "    chardelay-max: 5000000",
               "    sendon: \"\\\\r\\\\n\""),
              "tcp,localhost,3023",
              "serialdev,/dev/ttyPipeB0,9600N81")
try:
    io1.handler.set_compare("test1")
    io2.handler.set_write_data("test1")
    if io1.handler.wait_timeout(250) != 0:
        raise Exception("sendon: Got data transfer incorrectly")
    io1.handler.set_compare("test1\r\n")
    io2.handler.set_write_data("\r\n")
    if io1.handler.wait_timeout(1000) == 0:
        raise Exception("closestr: Timed out waiting for sendon")
finally:
    utils.finish_2_ser2net(ser2net, io1, io2)

print("  Success!")
