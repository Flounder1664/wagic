#!/bin/sh
# Lists branches carrying commits that trunk does not have.
#
# The point is to catch divergence while it is one day old and a clean merge, rather than
# six weeks old and two different games. Run it before finishing a session, and before
# building.
#
# Exit status is the number of diverged branches, so it can gate a build:
#   ./tools/check-branch-divergence.sh || echo "merge these first"

TRUNK=${TRUNK:-wagic-v146-windows}

if ! git rev-parse --verify --quiet "$TRUNK" >/dev/null; then
    echo "check-branch-divergence: no such branch '$TRUNK'" >&2
    exit 125
fi

n=0
printf '%-46s %7s %7s  %s\n' BRANCH AHEAD BEHIND "LAST COMMIT"
for b in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
    [ "$b" = "$TRUNK" ] && continue
    case "$b" in
        wip/*|master) continue ;;   # parked or upstream: divergence there is intentional
    esac
    ahead=$(git rev-list --count "$TRUNK".."$b")
    [ "$ahead" -eq 0 ] && continue
    behind=$(git rev-list --count "$b".."$TRUNK")
    printf '%-46s %7s %7s  %s\n' "$b" "$ahead" "$behind" "$(git log -1 --format=%cs "$b")"
    n=$((n + 1))
done

if [ "$n" -eq 0 ]; then
    echo "(nothing unmerged - trunk has everything)"
else
    echo
    echo "$n branch(es) have work trunk does not. Merge them into $TRUNK, do not re-port by hand."
fi

exit "$n"
