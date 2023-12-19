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
        "TTT": "TT",
        "TTL": "TT",
        "TTJ": "TT",
        "VVT": "VV",
        "VVL": "VV",
        "VVJ": "VV",
        "W": "W",
        "EMB": "EMB",
        "QCDEMB": "QCD",
        "QCD": "QCDMC",
        "jetFakesEMB": "jetFakes",
        "jetFakes": "jetFakesMC",
        "ggH125": "ggH",
        "qqH125": "qqH",
        "wFakes": "wFakes",
        "embminus2p5": "embminus2p5",
        "embminus2p4": "embminus2p4",
        "embminus2p3": "embminus2p3",
        "embminus2p2": "embminus2p2",
        "embminus2p1": "embminus2p1",
        "embminus2p0": "embminus2p0",
        "embminus1p9": "embminus1p9",
        "embminus1p8": "embminus1p8",
        "embminus1p7": "embminus1p7",
        "embminus1p6": "embminus1p6",
        "embminus1p5": "embminus1p5",
        "embminus1p4": "embminus1p4",
        "embminus1p3": "embminus1p3",
        "embminus1p2": "embminus1p2",
        "embminus1p1": "embminus1p1",
        "embminus1p0": "embminus1p0",
        "embminus0p9": "embminus0p9",
        "embminus0p8": "embminus0p8",
        "embminus0p7": "embminus0p7",
        "embminus0p6": "embminus0p6",
        "embminus0p5": "embminus0p5",
        "embminus0p4": "embminus0p4",
        "embminus0p3": "embminus0p3",
        "embminus0p2": "embminus0p2",
        "embminus0p1": "embminus0p1",
        "emb0p0": "emb0p0",
        "emb0p1": "emb0p1",
        "emb0p2": "emb0p2",
        "emb0p3": "emb0p3",
        "emb0p4": "emb0p4",
        "emb0p5": "emb0p5",
        "emb0p6": "emb0p6",
        "emb0p7": "emb0p7",
        "emb0p8": "emb0p8",
        "emb0p9": "emb0p9",
        "emb1p0": "emb1p0",
        "emb1p1": "emb1p1",
        "emb1p2": "emb1p2",
        "emb1p3": "emb1p3",
        "emb1p4": "emb1p4",
        "emb1p5": "emb1p5",
        "emb1p6": "emb1p6",
        "emb1p7": "emb1p7",
        "emb1p8": "emb1p8",
        "emb1p9": "emb1p9",
        "emb2p0": "emb2p0",
        "emb2p1": "emb2p1",
        "emb2p2": "emb2p2",
        "emb2p3": "emb2p3",
        "emb2p4": "emb2p4",
        "emb2p5": "emb2p5",
    }

    _process_map = {
        "data": "data",
        "ZTT": "DY-ZTT",
        "ZL": "DY-ZL",
        "ZJ": "DY-ZJ",
        "TTT": "TT-TTT",
        "TTL": "TT-TTL",
        "TTJ": "TT-TTJ",
        "VVT": "VV-VVT",
        "VVL": "VV-VVL",
        "VVJ": "VV-VVJ",
        "W": "W",
        "EMB": "Embedded",
        "QCDEMB": "QCD",
        "QCD": "QCDMC",
        "jetFakesEMB": "jetFakes",
        "jetFakes": "jetFakesMC",
        "ggH125": "ggH125",
        "qqH125": "qqH125",
        "wFakes": "wFakes",
        "embminus2p5": "Embedded",
        "embminus2p4": "Embedded",
        "embminus2p3": "Embedded",
        "embminus2p2": "Embedded",
        "embminus2p1": "Embedded",
        "embminus2p0": "Embedded",
        "embminus1p9": "Embedded",
        "embminus1p8": "Embedded",
        "embminus1p7": "Embedded",
        "embminus1p6": "Embedded",
        "embminus1p5": "Embedded",
        "embminus1p4": "Embedded",
        "embminus1p3": "Embedded",
        "embminus1p2": "Embedded",
        "embminus1p1": "Embedded",
        "embminus1p0": "Embedded",
        "embminus0p9": "Embedded",
        "embminus0p8": "Embedded",
        "embminus0p7": "Embedded",
        "embminus0p6": "Embedded",
        "embminus0p5": "Embedded",
        "embminus0p4": "Embedded",
        "embminus0p3": "Embedded",
        "embminus0p2": "Embedded",
        "embminus0p1": "Embedded",
        "emb0p0": "Embedded",
        "emb0p1": "Embedded",
        "emb0p2": "Embedded",
        "emb0p3": "Embedded",
        "emb0p4": "Embedded",
        "emb0p5": "Embedded",
        "emb0p6": "Embedded",
        "emb0p7": "Embedded",
        "emb0p8": "Embedded",
        "emb0p9": "Embedded",
        "emb1p0": "Embedded",
        "emb1p1": "Embedded",
        "emb1p2": "Embedded",
        "emb1p3": "Embedded",
        "emb1p4": "Embedded",
        "emb1p5": "Embedded",
        "emb1p6": "Embedded",
        "emb1p7": "Embedded",
        "emb1p8": "Embedded",
        "emb1p9": "Embedded",
        "emb2p0": "Embedded",
        "emb2p1": "Embedded",
        "emb2p2": "Embedded",
        "emb2p3": "Embedded",
        "emb2p4": "Embedded",
        "emb2p5": "Embedded",
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
