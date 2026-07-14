#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import ROOT
import copy

logger = logging.getLogger(__name__)


class Rootfile_parser(object):
    _dataset_map = {
        "data": "data",
        "ZTT": "DY",
        "ZL": "DY",
        "ZJ": "DY",
        "ZTT_NLO": "DYNLO",
        "ZL_NLO": "DYNLO",
        "ZJ_NLO": "DYNLO",
        "TTT": "TT",
        "TTL": "TT",
        "TTJ": "TT",
        "VVT": "VV",
        "VVL": "VV",
        "VVJ": "VV",
        "W": "W",
        "W_NLO": "WNLO",
        "EMB": "EMB",
        "QCDEMB": "QCD",
        "QCD": "QCDMC",
        "jetFakesEMB": "jetFakes",
        "jetFakes": "jetFakesMC",
        "QCDEMB_NLO": "QCD_NLO",
        "QCD_NLO": "QCDMC_NLO",
        "jetFakesEMB_NLO": "jetFakes_NLO",
        "jetFakes_NLO": "jetFakesMC_NLO",
        "ggH125": "ggH",
        "qqH125": "qqH",
        "VH125": "VH",
        "ttH125": "ttH",
        "wFakes": "wFakes",
    }

    _process_map = {
        "data": "data",
        "ZTT": "DY-ZTT",
        "ZL": "DY-ZL",
        "ZJ": "DY-ZJ",
        "ZTT_NLO": "DY_NLO-ZTT",
        "ZL_NLO": "DY_NLO-ZL",
        "ZJ_NLO": "DY_NLO-ZJ",
        "TTT": "TT-TTT",
        "TTL": "TT-TTL",
        "TTJ": "TT-TTJ",
        "VVT": "VV-VVT",
        "VVL": "VV-VVL",
        "VVJ": "VV-VVJ",
        "W": "W",
        "W_NLO": "W",
        "EMB": "Embedded",
        "QCDEMB": "QCD",
        "QCD": "QCDMC",
        "QCDEMB_NLO": "QCD_NLO",
        "QCD_NLO": "QCDMC_NLO",
        "jetFakesEMB": "jetFakes",
        "jetFakes": "jetFakesMC",
        "ggH125": "ggH125",
        "qqH125": "qqH125",
        "VH125": "VH125",
        "ttH125": "ttH125",
        "wFakes": "wFakes",
    }

    def __init__(self, inputrootfilename, variable):
        self._variable = variable
        # Accept both a single string and a list
        if isinstance(inputrootfilename, str):
            inputrootfilename = [inputrootfilename]
        self._rootfilenames = inputrootfilename
        self._rootfiles = [ROOT.TFile(f, "READ") for f in self._rootfilenames]
        # Keep backward compat: expose first file as .rootfile
        self._rootfile = self._rootfiles[0]

    def get(self, channel, process, category=None, shape_type="Nominal"):
        dataset = self._dataset_map[process]
        if category is None:
            category = "" if "data" in process else "-" + self._process_map[process]
        else:
            category = (
                "-" + category
                if "data" in process
                else "-" + "-".join([self._process_map[process], category])
            )
        hist_hash = "{dataset}#{channel}{category}#{shape_type}#{variable}".format(
            dataset=dataset,
            channel=channel,
            category=category,
            shape_type=shape_type,
            variable=self._variable,
        )
        logger.debug("Try to access %s" % hist_hash)

        combined = None
        for rootfile in self._rootfiles:
            h = rootfile.Get(hist_hash)
            if not h:
                logger.warning("Hash %s not found in %s" % (hist_hash, rootfile.GetName()))
                continue
            if combined is None:
                combined = copy.deepcopy(h)  # deepcopy so we don't modify the in-file object
            else:
                combined.Add(h)

        print("rootfile: ", combined, " hash: ", hist_hash)
        return combined

    def __del__(self):
        for f in self._rootfiles:
            logger.debug("Closing rootfile %s" % f.GetName())
            f.Close()
