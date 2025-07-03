document.addEventListener("DOMContentLoaded", function () {
  window.updateUserRole = async function (userId, newRole) {
    await makeRequest(window.userManagementPageUrl, 'POST', {
      user_id: userId,
      role: newRole
    });
  };

  async function makeRequest(url, method, body) {
    let headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': window.csrftoken
    };

    return fetch(url, {
      method: method,
      headers: headers,
      body: JSON.stringify(body)
    })
    .then(async response => {
      let data = await response.json();
      let status = await data.status;
      if (status === "success") {
        toastr.success("Role updated successfully");
      } else {
        toastr.error("An error occurred while updating the role");
      }
    });
  }
});