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
        "STT": "ST",
        "STL": "ST",
        "STJ": "ST",
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
        "wFakes": "wFakes",
        "embminus8p0": "embminus8p0", "embminus7p9": "embminus7p9", "embminus7p8": "embminus7p8", "embminus7p7": "embminus7p7", "embminus7p6": "embminus7p6",
        "embminus7p5": "embminus7p5", "embminus7p4": "embminus7p4", "embminus7p3": "embminus7p3", "embminus7p2": "embminus7p2", "embminus7p1": "embminus7p1",
        "embminus7p0": "embminus7p0", "embminus6p9": "embminus6p9", "embminus6p8": "embminus6p8", "embminus6p7": "embminus6p7", "embminus6p6": "embminus6p6",
        "embminus6p5": "embminus6p5", "embminus6p4": "embminus6p4", "embminus6p3": "embminus6p3", "embminus6p2": "embminus6p2", "embminus6p1": "embminus6p1",
        "embminus6p0": "embminus6p0", "embminus5p9": "embminus5p9", "embminus5p8": "embminus5p8", "embminus5p7": "embminus5p7", "embminus5p6": "embminus5p6",
        "embminus5p5": "embminus5p5", "embminus5p4": "embminus5p4", "embminus5p3": "embminus5p3", "embminus5p2": "embminus5p2", "embminus5p1": "embminus5p1",
        "embminus5p0": "embminus5p0", "embminus4p9": "embminus4p9", "embminus4p8": "embminus4p8", "embminus4p7": "embminus4p7", "embminus4p6": "embminus4p6",
        "embminus4p5": "embminus4p5", "embminus4p4": "embminus4p4", "embminus4p3": "embminus4p3", "embminus4p2": "embminus4p2", "embminus4p1": "embminus4p1",
        "embminus4p0": "embminus4p0", "embminus3p9": "embminus3p9", "embminus3p8": "embminus3p8", "embminus3p7": "embminus3p7", "embminus3p6": "embminus3p6",
        "embminus3p5": "embminus3p5", "embminus3p4": "embminus3p4", "embminus3p3": "embminus3p3", "embminus3p2": "embminus3p2", "embminus3p1": "embminus3p1",
        "embminus3p0": "embminus3p0", "embminus2p9": "embminus2p9", "embminus2p8": "embminus2p8", "embminus2p7": "embminus2p7", "embminus2p6": "embminus2p6",
        "embminus2p5": "embminus2p5", "embminus2p4": "embminus2p4", "embminus2p3": "embminus2p3", "embminus2p2": "embminus2p2", "embminus2p1": "embminus2p1",
        "embminus2p0": "embminus2p0", "embminus1p9": "embminus1p9", "embminus1p8": "embminus1p8", "embminus1p7": "embminus1p7", "embminus1p6": "embminus1p6",
        "embminus1p5": "embminus1p5", "embminus1p4": "embminus1p4", "embminus1p3": "embminus1p3", "embminus1p2": "embminus1p2", "embminus1p1": "embminus1p1",
        "embminus1p0": "embminus1p0", "embminus0p9": "embminus0p9", "embminus0p8": "embminus0p8", "embminus0p7": "embminus0p7", "embminus0p6": "embminus0p6",
        "embminus0p5": "embminus0p5", "embminus0p4": "embminus0p4", "embminus0p3": "embminus0p3", "embminus0p2": "embminus0p2", "embminus0p1": "embminus0p1",
        "emb0p0": "emb0p0", "emb0p1": "emb0p1", "emb0p2": "emb0p2", "emb0p3": "emb0p3", "emb0p4": "emb0p4", "emb0p5": "emb0p5", "emb0p6": "emb0p6",
        "emb0p7": "emb0p7", "emb0p8": "emb0p8", "emb0p9": "emb0p9", "emb1p0": "emb1p0", "emb1p1": "emb1p1", "emb1p2": "emb1p2", "emb1p3": "emb1p3",
        "emb1p4": "emb1p4", "emb1p5": "emb1p5", "emb1p6": "emb1p6", "emb1p7": "emb1p7", "emb1p8": "emb1p8", "emb1p9": "emb1p9", "emb2p0": "emb2p0",
        "emb2p1": "emb2p1", "emb2p2": "emb2p2", "emb2p3": "emb2p3", "emb2p4": "emb2p4", "emb2p5": "emb2p5",
        "emb2p6": "emb2p6", "emb2p7": "emb2p7", "emb2p8": "emb2p8", "emb2p9": "emb2p9", "emb3p0": "emb3p0",
        "emb3p1": "emb3p1", "emb3p2": "emb3p2", "emb3p3": "emb3p3", "emb3p4": "emb3p4", "emb3p5": "emb3p5",
        "emb3p6": "emb3p6", "emb3p7": "emb3p7", "emb3p8": "emb3p8", "emb3p9": "emb3p9", "emb4p0": "emb4p0"
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
        "STT": "ST-STT",
        "STL": "ST-STL",
        "STJ": "ST-STJ",
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
        "wFakes": "wFakes",
        "embminus8p0": "Embedded", "embminus7p9": "Embedded", "embminus7p8": "Embedded", "embminus7p7": "Embedded", "embminus7p6": "Embedded",
        "embminus7p5": "Embedded", "embminus7p4": "Embedded", "embminus7p3": "Embedded", "embminus7p2": "Embedded", "embminus7p1": "Embedded",
        "embminus7p0": "Embedded", "embminus6p9": "Embedded", "embminus6p8": "Embedded", "embminus6p7": "Embedded", "embminus6p6": "Embedded",
        "embminus6p5": "Embedded", "embminus6p4": "Embedded", "embminus6p3": "Embedded", "embminus6p2": "Embedded", "embminus6p1": "Embedded",
        "embminus6p0": "Embedded", "embminus5p9": "Embedded", "embminus5p8": "Embedded", "embminus5p7": "Embedded", "embminus5p6": "Embedded",
        "embminus5p5": "Embedded", "embminus5p4": "Embedded", "embminus5p3": "Embedded", "embminus5p2": "Embedded", "embminus5p1": "Embedded",
        "embminus5p0": "Embedded", "embminus4p9": "Embedded", "embminus4p8": "Embedded", "embminus4p7": "Embedded", "embminus4p6": "Embedded",
        "embminus4p5": "Embedded", "embminus4p4": "Embedded", "embminus4p3": "Embedded", "embminus4p2": "Embedded", "embminus4p1": "Embedded",
        "embminus4p0": "Embedded", "embminus3p9": "Embedded", "embminus3p8": "Embedded", "embminus3p7": "Embedded", "embminus3p6": "Embedded",
        "embminus2p0": "Embedded", "embminus1p9": "Embedded", "embminus1p8": "Embedded", "embminus1p7": "Embedded", "embminus1p6": "Embedded",
        "embminus3p5": "Embedded", "embminus3p4": "Embedded", "embminus3p3": "Embedded", "embminus3p2": "Embedded", "embminus3p1": "Embedded",
        "embminus2p5": "Embedded", "embminus2p4": "Embedded", "embminus2p3": "Embedded", "embminus2p2": "Embedded", "embminus2p1": "Embedded",
        "embminus3p0": "Embedded", "embminus2p9": "Embedded", "embminus2p8": "Embedded", "embminus2p7": "Embedded", "embminus2p6": "Embedded",
        "embminus1p5": "Embedded", "embminus1p4": "Embedded", "embminus1p3": "Embedded", "embminus1p2": "Embedded", "embminus1p1": "Embedded",
        "embminus1p0": "Embedded", "embminus0p9": "Embedded", "embminus0p8": "Embedded", "embminus0p7": "Embedded", "embminus0p6": "Embedded",
        "embminus0p5": "Embedded", "embminus0p4": "Embedded", "embminus0p3": "Embedded", "embminus0p2": "Embedded", "embminus0p1": "Embedded",
        "emb0p0": "Embedded", "emb0p1": "Embedded", "emb0p2": "Embedded", "emb0p3": "Embedded", "emb0p4": "Embedded", "emb0p5": "Embedded", "emb0p6": "Embedded",
        "emb0p7": "Embedded", "emb0p8": "Embedded", "emb0p9": "Embedded", "emb1p0": "Embedded", "emb1p1": "Embedded", "emb1p2": "Embedded", "emb1p3": "Embedded",
        "emb1p4": "Embedded", "emb1p5": "Embedded", "emb1p6": "Embedded", "emb1p7": "Embedded", "emb1p8": "Embedded", "emb1p9": "Embedded", "emb2p0": "Embedded",
        "emb2p1": "Embedded", "emb2p2": "Embedded", "emb2p3": "Embedded", "emb2p4": "Embedded", "emb2p5": "Embedded",
        "emb2p6": "Embedded", "emb2p7": "Embedded", "emb2p8": "Embedded", "emb2p9": "Embedded", "emb3p0": "Embedded",
        "emb3p1": "Embedded", "emb3p2": "Embedded", "emb3p3": "Embedded", "emb3p4": "Embedded", "emb3p5": "Embedded",
        "emb3p6": "Embedded", "emb3p7": "Embedded", "emb3p8": "Embedded", "emb3p9": "Embedded", "emb4p0": "Embedded"
    }

    def __init__(self, inputrootfilename, variable):
        self._rootfilename = inputrootfilename
        self._rootfile = ROOT.TFile(self._rootfilename, "READ")
        self._variable = variable

    @property
    def rootfile(self):
        return self._rootfile

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
        logger.debug("Try to access %s in %s" % (hist_hash, self._rootfilename))
        print("rootfile: ", self._rootfile.Get(hist_hash), " hash: ", hist_hash)

        return self._rootfile.Get(hist_hash)

    def list_contents(self):
        return [key.GetTitle() for key in self._rootfile.GetListOfKeys()]

    def get_bins(self, channel, category):
        hist = self.get(channel, category)
        nbins = hist.GetNbinsX()
        bins = []
        for i in range(nbins):
            bins.append(hist.GetBinLowEdge(i + 1))
        bins.append(hist.GetBinLowEdge(i + 1) + hist.GetBinWidth(i + 1))
        return bins

    def get_values(self, channel, category):
        hist = self.get(channel, category)
        nbins = hist.GetNbinsX()
        values = []
        for i in range(nbins):
            values.append(hist.GetBinContent(i + 1))
        return values

    def __del__(self):
        logger.debug("Closing rootfile %s" % (self._rootfilename))
        self._rootfile.Close()
