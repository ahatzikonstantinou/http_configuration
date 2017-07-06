#!/usr/bin/env python
import web
import json
import os.path # to check if configuration file exists


def notfound():
    #return web.notfound("Sorry, the page you were looking for was not found.")
    return json.dumps({'ok':0, 'errcode': 404})

def internalerror():
    #return web.internalerror("Bad, bad server. No donut for you.")
    return json.dumps({'ok':0, 'errcode': 500})

def badData():
    return json.dumps( { 'ok': 0, 'errcode': 400 } )

urls = (
    '/configuration(.*)', 'configuration',
    '/translate(.*)', 'translate'
)


app = web.application(urls, globals())
app.notfound = notfound
app.internalerror = internalerror

class configuration:
    ConfigurationFile = 'configuration.json'
    def GET( self, params ):        
        queryString = web.input()
        print( queryString )
        if( not os.path.isfile( configuration.ConfigurationFile ) ):
            print( 'Configuration file "{}" not found, exiting.'.format( configuration.ConfigurationFile ) )
            return internalerror()

        with open( configuration.ConfigurationFile ) as json_file:
            configurationTxt = json.load( json_file )
            # print( 'Configuration: \n{}', json.dumps( configurationTxt ) )
            # the response must have this particular format due to angular quirks see https://stackoverflow.com/questions/11574850/jsonp-web-service-with-python
            return '{0}({1})'.format( queryString.callback, json.dumps( configurationTxt, indent=2 ) )

    def POST( self ):
        data = web.data()
        print( data )
        try:
            json.loads( data )
        except:
            return badData()

        try:
            with open( configuration.ConfigurationFile, 'w' ) as outfile:
                json.dump( data, outfile )
        except:
            internalerror()
        
        return json.dumps( { 'ok': 200, 'errcode': 0 } )

class Translation( object ):
    def __init__( self ):
        self.house = ''
        self.floor = ''
        self.room = ''
        self.domain = ''
        self.item = ''

class translate:
    def GET( self, params ):
        params = web.input()
        print( params )
        if( params.item is None ):
            return badData()

        try:
            with open( configuration.ConfigurationFile ) as json_file:
                configurationTxt = json.load( json_file )
        except:
            return internalerror()
                        
        translation = self.__findTranslation( params.item, configurationTxt )
        
        if( translation is None ):
            return notfound()

        # return '{0}({1})'.format( params.callback, json.dumps( translation, indent=2 ) )

        return json.dumps( { 'house': translation.house, 'floor': translation.floor, 'room': translation.room, 'domain': translation.domain, 'item': translation.item }, indent=2 )


    def __findTranslation( self, translate, configurationTxt ):
        # print( configurationTxt )
        translation = Translation()
        sections = translate.split( "/" )
        house = sections[0]
        if( len( house ) > 0 ):
            for h in range( 0, len( configurationTxt ) ):
                if( 'mqtt' in configurationTxt[h] ):
                    print( configurationTxt[h]['mqtt'] )
                # for key in configurationTxt[h]:
                #     print( key )
                    if( configurationTxt[h]['mqtt'] == house ):
                        translation.house = configurationTxt[h][ 'name' ]
                        print( translation )

                        TODO

        print( sections )
        return translation


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()