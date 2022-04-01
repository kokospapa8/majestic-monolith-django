#!/usr/bin/env python3
import os

import aws_cdk as cdk
from mmd_app.mmd_app_stack import MmdAppStack

app = cdk.App()
MmdAppStack(
    app,
    "MmdAppStack",
)

app.synth()
