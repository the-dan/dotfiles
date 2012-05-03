# settings homes, some of them we'll put into path
if [[ -x .paths ]]; then
	. .paths
fi

# apply local profile
if [[ -x .profile.local ]]; then
    . .profile.local
fi


SSH_ENV="$HOME/.ssh/environment"

function start_agent {
	echo "Initializing new SSH agent..."
	/usr/bin/ssh-agent -t 8h | sed 's/^echo/#echo/' > "${SSH_ENV}"
	echo succeeded
	chmod 600 "${SSH_ENV}"
	. "${SSH_ENV}" > /dev/null
	/usr/bin/ssh-add $KEYS_PATH;
}

if [ -f "${SSH_ENV}" ]; then
	. "${SSH_ENV}" > /dev/null
	ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent > /dev/null || {
		start_agent;
	}
else
	start_agent;
fi

function to_win()
{
    "`cygpath -wa $1`"
}

case `uname` in
Darwin)
	. .alias.mac
	LSCOLORS=cxfxfhdxbxegedabagacad
	;;
*)
	. .alias
	LS_COLORS="di=32;40:ln=35;40:so=35;47:pi=33;40:ex=31;40:bd=34;46:cd=34;43:su=0;41:sg=0;46:tw=0;42:ow=0;43:"
	;;
esac


alias df='df -h'
alias cgrep='grep -A 3 -B 3'

shopt -s histappend

export PS1="\n\[\e[32;1m\](\[\e[37;1m\]\u\[\e[32;1m\])-(\[\e[37;1m\]jobs:\j\[\e[32;1m\])-(\[\e[37;1m\]\w\[\e[32;1m\])\n(\[\[\e[37;1m\]! \!\[\e[32;1m\])-> \[\e[0m\]"

export PATH=$HOME/bin:$CURL_HOME:$SVN_HOME:$NSS_HOME/bin:$JAVA_HOME/bin:$GROOVY_HOME/bin:$PATH

