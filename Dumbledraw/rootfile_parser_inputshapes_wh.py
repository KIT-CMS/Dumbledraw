#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import ROOT
import copy

logger = logging.getLogger(__name__)
import yaml


class Rootfile_parser(object):

    _dataset_map = {
        "data": "data",
        "ggZZ": "ggZZ",
        "VHWW": "rem_VH",
        "rem_VV": "rem_VV",
        "TTV": "rem_ttbar",
        "WWZ": "WWZ",
        "WZZ": "WZZ",
        "WWW": "WWW",
        "ZZZ": "ZZZ",
        "WHplus": "WHplus",
        "WHminus": "WHminus",
        "ZH": "ZH",
        "ZZ": "ZZ",
        "WZ": "WZ",
        "TT": "TT",
        "Wjets": "Wjets",
        "DY": "DY",
        "jetFakes": "jetFakes",
    }
    _process_map = {
        "data": "data",
        "jetFakes": "jetFakes",
        "ggZZ": "VV",
        "WWZ": "WWZ",
        "WZZ": "WZZ",
        "WWW": "WWW",
        "ZZZ": "ZZZ",
        "VHWW": "VH",
        "WHplus": "VH",
        "WHminus": "VH",
        "ZH": "VH",
        "WZ": "VV",
        "ZZ": "VV",
        "TT": "TT",
        "TTV": "TT",
        "Wjets": "W",
        "DY": "DY",
        "rem_VV": "VV",
        "QCD": "QCDMC",
    }

    def __init__(self, inputrootfilename, variable):
        print(inputrootfilename)
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
