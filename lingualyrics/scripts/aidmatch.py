import acoustid
import sys

# http://acoustid.org/
API_KEY = 'HEywukPjo9'


def aidmatch(filename, callback):
    results = iter(())
    try:
        results = acoustid.match(API_KEY, filename)
    except acoustid.NoBackendError:
        print("chromaprint library/tool not found") 
    except acoustid.FingerprintGenerationError:
        print("fingerprint could not be calculated")
    except acoustid.WebServiceError as exc:
        print("web service request failed:")

    callback(results)


if __name__ == '__main__':
    aidmatch(sys.argv[1])