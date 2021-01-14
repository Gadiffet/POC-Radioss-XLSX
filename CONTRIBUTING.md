#How to Contribute

Creat a Branch to resolve an Issue.
Respect the Format of the Commit Message.

## Branching conventions
You must create a branch with the name of the Issue.

#The Format of the Commit Message
Format of the commit message

    <type>(<scope>): <subject>

Any line of the commit message cannot be longer 100 characters! This allows the message to be easier to read on github as well as in various git tools.
Subject line

Subject line contains succinct description of the change.
Allowed `<type>`

    feat (feature)
    fix (bug fix)
    docs (documentation)
    style (formatting, missing semi colons, …)
    refactor
    test (when adding missing tests)
    confs (configuration)
    chore (maintain)

Allowed `<scope>`

Scope could be anything specifying place of the commit change.

For code based, all scope must be a valid gradle subproject for the current project. For example :

    fix(error):Fix error 400

For docs, since we have only readme, the only scope allowed is readme
`<subject>` text

- use imperative, present tense: “change” not “changed” nor “changes”
- don't capitalize first letter
- no dot (.) at the end
