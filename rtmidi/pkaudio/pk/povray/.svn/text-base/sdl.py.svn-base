import sys, os

class File:
    def __init__(self, fname, *items):
        self.file = open(fname, 'w')
        self.__indent = 0
        self.write(*items)

    def include(self,name):
        self.writeln( '#include "%s"'%name )
        self.writeln()

    def indent(self):
        self.__indent += 1

    def dedent(self):
        self.__indent -= 1
        assert self.__indent >= 0

    def block_begin(self):
        self.writeln( "{" )
        self.indent()

    def block_end(self):
        self.dedent()
        self.writeln( "}" )
        if self.__indent == 0:
            # blank line if this is a top level end
            self.writeln( )

    def write(self,*items):
        for item in items:
            if type(item) == str:
                self.include(item)
            else:
                item.write(self)

    def writeln(self,s=""):
        #print "  "*self.__indent+s
        self.file.write("  "*self.__indent+s+os.linesep)

class Vector:
    def __init__(self,*args):
        if len(args) == 1:
            self.v = args[0]
        else:
            self.v = args
    def __str__(self):
        return "<%s>"%(", ".join([str(x)for x in self.v]))
    def __repr__(self):
        return "Vector(%s)"%self.v
    def __mul__(self,other):
        return Vector( [r*other for r in self.v] )
    def __rmul__(self,other):
        return Vector( [r*other for r in self.v] )

class Item:
    def __init__(self,name,args=[],opts=[],**kwargs):
        self.name = name
        args=list(args)
        for i in range(len(args)):
            if type(args[i]) == tuple or type(args[i]) == list:
                args[i] = Vector(args[i])
        self.args = args
        self.opts = opts
        self.kwargs = kwargs
        self._timer = None

    def append(self, item):
        self.opts.append( item )

    def write(self, file):
        file.writeln( self.name )
        file.block_begin()
        if self.args:
            file.writeln( ", ".join([str(arg) for arg in self.args]) )
        for opt in self.opts:
            if hasattr(opt,"write"):
                opt.write(file)
            else:
                file.writeln( str(opt) )
        for key,val in self.kwargs.items():
            if type(val)==tuple or type(val)==list:
                val = Vector(*val)
                file.writeln( "%s %s"%(key,val) )
            else:
                if isinstance(val, Item):
                    val.write(file)
                else:
                    file.writeln( "%s %s"%(key,val) )
        file.block_end()
        
    def __setattr__(self,name,val):
        self.__dict__[name]=val
        if not name.startswith('_') and name not in ["kwargs","args","opts","name"]:
            self.__dict__["kwargs"][name]=val
            
    def __setitem__(self,i,val):
        if i < len(self.args):
            self.args[i] = val
        else:
            i += len(args)
            if i < len(self.opts):
                self.opts[i] = val
                
    def __getitem__(self,i,val):
        if i < len(self.args):
            return self.args[i]
        else:
            i += len(args)
            if i < len(self.opts):
                return self.opts[i]


class Texture(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"texture",(),opts,**kwargs)

class Pigment(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"pigment",(),opts,**kwargs)

class Finish(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"finish",(),opts,**kwargs)

class Normal(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"normal",(),opts,**kwargs)

class Camera(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"camera",(),opts,**kwargs)

class LightSource(Item):
    def __init__(self,v,*opts,**kwargs):
        Item.__init__(self,"light_source",(Vector(v),),opts,**kwargs)

class Background(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"background",(),opts,**kwargs)

class Box(Item):
    def __init__(self,v1,v2,*opts,**kwargs):
        #self.v1 = Vector(v1)
        #self.v2 = Vector(v2)
        Item.__init__(self,"box",(v1,v2),opts,**kwargs)

class Cylinder(Item):
    def __init__(self,v1,v2,r,*opts,**kwargs):
        " opts: open "
        Item.__init__(self,"cylinder",(v1,v2,r),opts,**kwargs)

class Plane(Item):
    def __init__(self,v,r,*opts,**kwargs):
        Item.__init__(self,"plane",(v,r),opts,**kwargs)

class Torus(Item):
    def __init__(self,r1,r2,*opts,**kwargs):
        Item.__init__(self,"torus",(r1,r2),opts,**kwargs)

class Cone(Item):
    def __init__(self,v1,r1,v2,r2,*opts,**kwargs):
        " opts: open "
        Item.__init__(self,"cone", (v1,r1,v2,r2),opts,**kwargs)

class Sphere(Item):
    def __init__(self,v,r,*opts,**kwargs):
        Item.__init__(self,"sphere",(v,r),opts,**kwargs)

class SuperEllipsoid(Item):
    def __init__(self, r1, r2, *opts, **kwargs):
        Item.__init__(self, "superellipsoid", (Vector(r1, r2),), opts, **kwargs)

class Union(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"union",(),opts,**kwargs)
    
class Intersection(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"intersection",(),opts,**kwargs)

class Difference(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"difference",(),opts,**kwargs)

class Merge(Item):
    def __init__(self,*opts,**kwargs):
        Item.__init__(self,"merge",(),opts,**kwargs)


class Scene:
    def __init__(self, *objects):
        self.objects = list(*objects)
        self.clock = 0.0

    def add(self, obj):
        if isinstance(obj, list):
            self.objects.extend(obj)
        else:
            self.objects.append(obj)
        return obj


POVRAY = 'povray +W266 +H200 +A0.3 +R2 +Q%(quality)s +K%(clock)s +SR%(start_row)s +ER%(end_row)s +SC%(start_col)s +EC%(end_col)s'

class Renderer:
    """ povray executable interface.
    setting clock, cmd line, etc goes here.
    """

    clock = 0.0
    quality = 3
    start_row=0
    end_row=200
    start_col=0
    end_col=266
    pause = False
    preview = False
    pretend = False

    def cmd_line_base(self):
        locals().update(self.__class__.__dict__)
        locals().update(self.__dict__)
        cmd = POVRAY % locals()
        if self.pause: cmd += ' +P'
        if not self.preview: cmd += ' -D'
        return cmd

    def write(self, scene, fpath):
        file = File(fpath)
        for o in scene.objects:
            if o._timer:
                o._timer(o, self.clock)
            o.write(file)

    def render(self, scene, povpath='__tmp.pov', pngpath='__tmp.png'):
        self.write(scene, povpath)
        cmd = self.cmd_line_base() + ' %s +O%s' % (povpath, pngpath)
        if self.pretend:
            print cmd
        else:
            run_safe(cmd)

def run_safe(cmd):
    """ sub-proc with keyboard interrupt. """
    print cmd
    name = cmd.split()[0]
    args = cmd.split()[1:]
    cmd = (os.P_WAIT, name, name) + tuple(args)
    try:
        ret = os.spawnlp(*cmd)
    except KeyboardInterrupt, e:
        return False
    if ret == 0: return True
    else: return False
