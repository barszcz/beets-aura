import mimetypes as default_mimetypes

class AcceptHeader(object):

    def __init__(self,mimetype,options={},mimetypes=default_mimetypes):
        self.mimetypes = mimetypes
        self.mimetype = mimetype
        self.mime_gentype, self.mime_subtype = self.mimetype.split('/')
        self.quality = options.pop('q', None)
        self.implicit_quality = None
        self.parameters = options
        self.extensions = mimetypes.guess_all_extensions(self.mimetype)

    def guess_extension(self):
        '''Guesses mimetype using python mimetypes package'''
        return self.mimetypes.guess_extension(self.mimetype)

    def matches(self, other):
        '''Returns True if 'other' mimetype is more general than self'''
        return (other.mime_gentype == '*' or
            (self.mime_gentype == other.mime_gentype
             and (other.mime_subtype == '*' or
                  (self.mime_subtype == other.mime_subtype
                   and len(self.parameters) <= len(other.parameters)))))

    def info(self):
        return '''AudioAcceptHeader({},{},{},{},{}, {})'''.format(
            self.mimetype, self.mime_gentype, self.mime_subtype,
            self.parameters, self.quality, self.implicit_quality)

    def precedence(self):
        '''Heuristic for precedence.

        Adds '1' for each level of specificity in mimetype'''
        prec = 0
        if self.mime_gentype != '*':
            prec += 1
        if self.mime_subtype != '*':
            prec += 1
        prec += len(self.parameters)
        return prec

    def __repr__(self):
        base_mime = self.mimetype
        if self.quality is not None:
            base_mime += "; q={}".format(self.quality)
        if self.parameters:
            base_mime += "; "
            base_mime += "; ".join(
                map(lambda x: "{}={}".format(x,self.parameters[x]),
                    self.parameters))
        return base_mime

    @classmethod
    def parse(cls,single_accept_str):
        '''Factory method from a single string with mimetype and parameters'''
        if ';' not in single_accept_str:
            return cls(single_accept_str)
        mime, params = single_accept_str.split(';',1)
        #print "MIME: {}, PARS: {}".format(mime, params)
        params_prsd = {
            k: float(v)
            for k,v in
            dict([p.strip().split('=') for p in params.split(';')]).iteritems()}
        return cls(mime.strip(),params_prsd)

    @classmethod
    def sort_key(cls):
        '''Returns function that sorts by quality (DESC) and then precedence (ASC)'''
        def sorter(hdr):
            quality = hdr.quality if hdr.quality is not None \
                      else hdr.implicit_quality
            return (-quality, #Sort by 'q' value, descending
                    hdr.precedence()) #Sort by specificity of type, asc


    @classmethod
    def guess_qualities(cls,headers):
        '''Guess implicit 'q' values according to W3C Spec.

        Unlabeled mimetypes are assigned a value of 'q' equal to the
        quality of the most specific, more general mimetype it belongs to,
        or defaults to 1.'''
        explicit = []
        implicit = []
        for h in headers:
            if h.quality is not None:
                explicit.append(h)
            else:
                implicit.append(h)
        for i in implicit:
            matching = filter(lambda h: i.matches(h), explicit)
            if matching:
                best_match = max(matching,key=lambda h: h.precedence())
                i.implicit_quality = best_match.quality
            else:
                i.implicit_quality = 1.0

def parse_accept_headers(accept_str, tree_filter=None):
    '''Parse 'Accept' Header into list of AcceptHeader objects'''
    headers = map(AcceptHeader.parse, accept_str.split(','))
    if tree_filter is not None:
        tf_header = AcceptHeader.parse(tree_filter)
        return filter(lambda h: h.matches(tf_header), headers)
    else:
        return headers

def sort_accept_headers(accept_str, tree_filter=None):
    '''Sort 'Accept' Headers by quality and specificity'''
    headers = parse_accept_headers(accept_str, tree_filter)
    AcceptHeader.guess_qualities(headers)
    #print headers[0].info()
    return sorted(headers, key=AcceptHeader.sort_key())

