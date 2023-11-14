# adi2edi
Minimalistic ADIF to REG1TEST/EDI converter for amateur radio operators

# DESCRIPTION:

Provide ADIF format as STDIN to this script or give a filename as `argv[1]`.
If the ADIF input is correct, it will produce a minimalistic EDI log file
with calculated QRB (claimed points)

# TODO:
- Check for new WWL's during the log generation
- Support RTTY/FT8 modes
- Multiply claimed points by band multiplier

# EXAMPLES:

    adi2edi.py < logfile.adif > logfile.edi

# REFERENCES:

https://www.ok2kkw.com/ediformat.htm
