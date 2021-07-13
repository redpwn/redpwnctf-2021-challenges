package main

import (
	"fmt"
	"net/http"
	"os"
	"strconv"
	"text/template"

	rctfgolf "github.com/redpwn/rctf-golf"
)

type templateArgs struct {
	Error  string
	Script string
	Length int
}

const htmlTemplateStr = `<!DOCTYPE html>
<html>
<head>
	<title>WTJS?!</title>
</head>
<body>
	<h1>Welcome to WTJS!</h1>
	<p>There's no real context to this challenge, it's just an exercise in JS golfing. Your input goes into a script tag, and your goal is to steal the admin's cookies!</p>
	<p>You're only allowed to use the characters <code>()*+=>[]_</code> in your code.</p>
	<p>Since this is a golf challenge, the number of characters you're allowed to use will slowly increase throughout the CTF. Currently, you are allowed {{ .Length }} characters.</p>
	<p>Good luck!</p>
	{{- with .Error }}
	<div style="color: red;">
		<h2>Error</h2>
		{{ . }}
	</div>
	{{- end }}
	<textarea id="payload"></textarea>
	<div id="chars"></div>
	<div id="info"></div>
	<button id="submit">Create!</button>
	<script>
		// BEGIN USER SCRIPT
		{{ .Script }}
		// END USER SCRIPT
		(() => {
			const maxLen = {{ .Length }}
			const charsTest = /^[\(\)\*\+=>\[\]_]*$/
			const eTa = document.getElementById('payload')
			const eChars = document.getElementById('chars')
			const eInfo = document.getElementById('info')
			const eSubmit = document.getElementById('submit')
			const onTaUpdate = () => {
				eTa.value = eTa.value.replace(/\n/g, '')
				const len = eTa.value.length
				eChars.innerText = len + '/' + maxLen
				if (len > maxLen || !eTa.value.match(charsTest)) {
					eChars.style.color = 'red'
					eSubmit.disabled = true
				} else {
					eChars.style.color = null
					eSubmit.disabled = false
				}
			}
			onTaUpdate()
			eTa.addEventListener('input', onTaUpdate)
			eSubmit.addEventListener('click', e => {
				e.preventDefault()
				window.location.search = '?script=' + encodeURIComponent(eTa.value)
			})
		})()
	</script>
</body>
</html>
`

func getLimit() (int, error) {
	elapsed, err := rctfgolf.GetTime("https://2021.redpwn.net", "wtjs")
	if err != nil {
		return 0, err
	}
	return int(elapsed.Minutes()/5) + 100, nil
}

func main() {
	port, err := strconv.Atoi(os.Getenv("PORT"))
	if err != nil {
		port = 8080
	}

	htmlTemplate, err := template.New("html").Parse(htmlTemplateStr)
	if err != nil {
		panic(err)
	}

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		limit, err := getLimit()
		if err != nil {
			w.WriteHeader(500)
			w.Write([]byte("Error computing limits, challenge (temporarily?) broken!"))
			fmt.Fprintln(os.Stderr, err.Error())
			return
		}
		r.ParseForm()
		script := ""
		if len(r.Form["script"]) > 0 {
			script = r.Form["script"][0]
		}
		if len(script) > limit {
			if err := htmlTemplate.Execute(w, templateArgs{Error: "Payload too long!", Length: limit}); err != nil {
				w.Write([]byte("Internal Server Error"))
				fmt.Fprintln(os.Stderr, err.Error())
				return
			}
			return
		}
		for _, ch := range script {
			if ch != '(' && ch != ')' && ch != '*' && ch != '+' && ch != '=' && ch != '>' && ch != '[' && ch != ']' && ch != '_' {
				w.WriteHeader(http.StatusBadRequest)
				if err := htmlTemplate.Execute(w, templateArgs{Error: fmt.Sprintf(`Illegal character: "%c"`, ch), Length: limit}); err != nil {
					w.Write([]byte("Internal Server Error"))
					fmt.Fprintln(os.Stderr, err.Error())
					return
				}
				return
			}
		}
		if err := htmlTemplate.Execute(w, templateArgs{Script: script, Length: limit}); err != nil {
			w.Write([]byte("Internal Server Error"))
			fmt.Fprintln(os.Stderr, err.Error())
			return
		}
	})

	http.HandleFunc("/favicon.ico", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	})

	fmt.Printf("Listening on port %d\n", port)
	if err := http.ListenAndServe(fmt.Sprintf(":%d", port), nil); err != nil {
		panic(err)
	}
}
