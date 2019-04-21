# -*- generated by 1.0.12 -*-
import da
PatternExpr_269 = da.pat.TuplePattern([da.pat.ConstantPattern('Request'), da.pat.FreePattern('sender')])
PatternExpr_386 = da.pat.TuplePattern([da.pat.ConstantPattern('Reply'), da.pat.FreePattern('type'), da.pat.FreePattern('sender'), da.pat.FreePattern('S')])
PatternExpr_782 = da.pat.ConstantPattern('Terminate')
PatternExpr_786 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.ConstantPattern('Terminate')])
_config_object = {}
import sys
import graph_config

class P(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._PReceivedEvent_2 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_0', PatternExpr_269, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_268]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_1', PatternExpr_386, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._P_handler_385]), da.pat.EventPattern(da.pat.ReceivedEvent, '_PReceivedEvent_2', PatternExpr_782, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, successors, own_id, all_processors, **rest_862):
        super().setup(successors=successors, own_id=own_id, all_processors=all_processors, **rest_862)
        self._state.successors = successors
        self._state.own_id = own_id
        self._state.all_processors = all_processors
        self._state.mode = 'sleep'
        self._state.status = 'undefined'
        self._state.num_suc = 0
        self._state.has_sent_cycle_message = False
        self._state.has_terminated_earlier = False
        self._state.earlier_reply_sent = ''
        self._state.this_S = {}
        self._state.result = 'unknown'
        self._state.parent = 0
        self._state.replies_received = {'cycle': 0, 'cycle_only': 0, 'incomplete_search': 0, 'leaf': 0}

    def run(self):
        self.initiate()
        super()._label('_st_label_779', block=False)
        _st_label_779 = 0
        while (_st_label_779 == 0):
            _st_label_779 += 1
            if PatternExpr_786.match_iter(self._PReceivedEvent_2, SELF_ID=self._id):
                _st_label_779 += 1
            else:
                super()._label('_st_label_779', block=True)
                _st_label_779 -= 1
        self.output('Done!!!')

    def initiate(self):
        if (self._state.own_id == 1):
            self._state.mode = 'awake'
            self._state.num_suc = len(self._state.successors)
            self.send(('Request', self._id), to=self._state.successors)
        else:
            self._state.mode = 'sleep'
            self._state.num_suc = 0

    def _P_handler_268(self, sender):

        def bar(i):
            return ((- 1) * i)
        S = set()
        if (self._state.own_id == 1):
            if self._state.has_sent_cycle_message:
                S.add(bar(self._state.own_id))
            self._state.has_sent_cycle_message = True
            self.send(('Reply', 'cycle', self._id, S), to=sender)
        elif self._state.has_terminated_earlier:
            self.send(('Reply', self._state.earlier_reply_sent, self._id, S), to=sender)
        elif (self._state.mode == 'awake'):
            self._state.earlier_reply_sent = 'incomplete_search'
            S = set()
            S.add(self._state.own_id)
            self.send(('Reply', 'incomplete_search', self._id, S), to=sender)
        elif (len(self._state.successors) == 0):
            S = set()
            self._state.earlier_reply_sent = 'leaf'
            self.send(('Reply', 'leaf', self._id, S), to=sender)
        else:
            self._state.parent = sender
            self._state.mode = 'awake'
            self._state.num_suc = len(self._state.successors)
            self.send(('Request', self._id), to=self._state.successors)
    _P_handler_268._labels = None
    _P_handler_268._notlabels = None

    def _P_handler_385(self, type, sender, S):

        def set_union(S1, S2):
            new_set = S1.union(S2)
            for i in new_set:
                if (i < 0):
                    if (((- 1) * i) in new_set):
                        new_set = new_set.remove(((- 1) * i))
            return new_set

        def type_exor(type1, type2):
            if ((type2 == 'cycle_only') or ((type1 == 'cycle') and (type2 == 'leaf')) or ((type1 == 'leaf') and (type2 == 'cycle'))):
                return 'cycle_only'
            elif (((type1 == 'cycle') and (type2 == 'incomplete_search')) or ((type2 == 'cycle') and (type1 == 'incomplete_search'))):
                return 'cycle'
            elif (((type1 == 'leaf') and (type2 == 'incomplete_search')) or ((type2 == 'leaf') and (type1 == 'incomplete_search'))):
                return 'leaf'
            else:
                self.output("Shouldn't come here!!!")
        if (self._state.own_id == 1):
            self._state.num_suc -= 1
            self._state.this_S[sender] = set_union(self._state.this_S[sender], S)
            self._state.status = type_exor(self._state.status, type)
            if (self._state.num_suc == 0):
                new_set = []
                for set_1j in self._state.this_S:
                    new_set = set_union(new_set, set_1j)
                unmarked_elements = [i for i in new_set if (i > 0)]
                self._state.has_terminated_earlier = True
                if (self._state.status == 'cycle_only'):
                    self._state.result = 'cycle'
                elif ((self._state.status == 'cycle') and (not new_set)):
                    (self._state.result == 'cycle')
                elif ((self._state.status == 'cycle') and (not unmarked_elements)):
                    self._state.result = 'knot'
                self.send('Terminate', to=self._state.all_processors)
        else:
            self._state.num_suc -= 1
            self._state.this_S[sender] = set_union(self._state.this_S[sender], S)
            self._state.status = type_exor(self._state.status, type)
            self._state.replies_received[type] = 1
            if (self._state.num_suc == 0):
                new_set = []
                for set_kj in self._state.this_S:
                    new_set = set_union(new_set, set_kj)
                self._state.has_terminated_earlier = True
                if (self._state.earlier_reply_sent == 'incomplete_search'):
                    new_set = set_union(new_set, [bar(self._state.own_id)])
                unmarked_elements = [i for i in new_set if (i > 0)]
                marked_elements = [i for i in new_set if (i < 0)]
                empty_set = set()
                if ((self._state.status == 'leaf') or ((self._state.status == 'incomplete_search') and (not unmarked_elements))):
                    self.send(('Reply', 'leaf', self._id, empty_set), to=self._state.parent)
                if ((self._state.status == 'incomplete_search') and unmarked_elements):
                    self.send(('Reply', 'incomplete_search', self._id, new_set), to=self._state.parent)
                if (self._state.status == 'cycle_only'):
                    self.send(('Reply', 'cycle_only', self._id, empty_set), to=self._state.parent)
                if (self._state.status == 'cycle'):
                    if ((self._state.replies_received['cycle'] == 1) and (self._state.replies_received['cycle_only'] == 0) and (self._state.replies_received['incomplete_search'] == 0) and (self._state.replies_received['leaf'] == 0)):
                        self.send(('Reply', 'cycle', self._id, new_set), to=self._state.parent)
                    elif (not unmarked_elements):
                        self.send(('Reply', 'cycle_only', self._id, new_set), to=self._state.parent)
                    else:
                        self.send(('Reply', 'cycle', self._id, new_set), to=self._state.parent)
    _P_handler_385._labels = None
    _P_handler_385._notlabels = None

class Node_(da.NodeProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._events.extend([])
    _config_object = {'channel': 'fifo'}

    def run(self):
        n = graph_config.network1['total_nodes']
        ps = list(self.new(P, num=n))
        for (i, p) in enumerate(ps):
            successors = [ps[(i - 1)] for i in graph_config.network1[('node' + str((i + 1)))]]
            self._setup({p}, (successors, (i + 1), ps))
        self._start(ps)
