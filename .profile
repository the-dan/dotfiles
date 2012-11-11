# settings homes, some of them we'll put into path
if [[ -x $HOME/.paths ]]; then
	. $HOME/.paths
fi

# apply local profile
if [[ -x $HOME/.profile.local ]]; then
    . $HOME/.profile.local
fi


SSH_DIR="$HOME/.ssh"
SSH_ENV="$HOME/.ssh/environment"

function start_agent {
	echo "Initializing new SSH agent..."
	if [ ! -d "${SSH_DIR}" ]; then
	    mkdir -p "${SSH_DIR}"
            chmod -R 700 "${SSH_DIR}"    	    
	fi

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

RED="\e[31m\]"
OFF="\e[0m\]"
FAILED_COMMAND_PS="\`RC=\$?; if [ \$RC != 0 ]; then echo -$RED\$RC$OFF; fi\`"

export PS1="\n\[\e[32;1m\](\[\e[37;1m\]\u@\h\[\e[32;1m\])-(\[\e[37;1m\]jobs:\j\[\e[32;1m\])-(\[\e[37;1m\]\W\[\e[32;1m\])-(\[\e[37;1m\]\A\[\e[32;1m\])$FAILED_COMMAND_PS\n(\[\[\e[37;1m\]! \!\[\e[32;1m\])-> \[\e[0m\]"

export PATH=$HOME/bin:$CURL_HOME:$SVN_HOME:$NSS_HOME/bin:$JAVA_HOME/bin:$GROOVY_HOME/bin:$PATH

if [ -x /usr/bin/emacs ]; then
    export EDITOR=/usr/bin/emacs
elif [ -x /usr/bin/vi ]; then
    export EDITOR=/usr/bin/vi
else
    export EDITOR=/usr/bin/nano
fi

alias e='$EDITOR'
