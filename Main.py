from GitUtil import GitUtil
import Commons

if __name__ == "__main__":
    print "Program starts"

    gitUtil = GitUtil('apache', 'commons-math')

    gitUtil.clone()

    tags = gitUtil.getTags()

    for tag in tags:
        name = tag['name']
        sha = tag['sha']
        # gitUtil.resetVersion(sha)

    print len(tags)