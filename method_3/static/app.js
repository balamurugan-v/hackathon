async function onSend() {
  let data = document.getElementById("messageInput");

  let message = data.value || "";

  const response = fetch("/new/message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  return response.then(() => (data.value = ""));
}

let eventSource = new EventSource("/listen");

eventSource.addEventListener(
  "message",
  function (e) {
    console.log(e, "message");

    let data = JSON.parse(e.data);

    const node = document.createElement("p");

    const textnode = document.createTextNode(data.message);

    node.appendChild(textnode);

    document.getElementById("messageWindow").appendChild(node);
    document.getElementById("messageWindow").scrollTop =
      document.getElementById("messageWindow").scrollHeight;
  },
  false
);
