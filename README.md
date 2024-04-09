# adi2edi
Minimalistic ADIF to REG1TEST/EDI converter for amateur radio operators

# DESCRIPTION:

Provide ADIF format as STDIN to this script or give a filename as `argv[1]`.
If the ADIF input is correct, it will produce a minimalistic EDI log file
with calculated QRB (claimed points)

# INSTALLATION

adi2edi requires Python3 - run the below commands:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


# TODO:
- Check for new WWL's during the log generation
- Support RTTY/FT8 modes
- Multiply claimed points by band multiplier

# EXAMPLE USAGE:

    ./adi2edi.py < logfile.adif > logfile.edi

# REFERENCES:

https://www.ok2kkw.com/ediformat.htm
