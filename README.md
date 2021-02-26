# PPP-OIRPOS
## Requirements
To run this you will need:
* keras 2.4.3+
* flask 1.1.2+
* pyqt  5.9.2+
* matplotlib 3.3.2+
* SQL Database

## API
Some endpoints used in application:
 <table style="width:100%">
  <tr>
    <th>Method</th>
    <th>Path</th>
    <th>Attributes</th>
    <th>Description/Response</th>
  </tr>
  <tr>
    <td>GET</td>
    <td>/</td>
    <td>-</td>
    <td>If user is logged returns its username otherwise redirect to login</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/login</td>
    <td>-</td>
    <td>articles[list]</td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/login</td>
    <td>username[string] login[string]</td>
    <td><b>id[int]</b> if credentials are correct redirect to <b>/</b> otherwise the error is returned</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/user/add</td>
    <td>-</td>
    <td>render template for <b>registration.html</b></td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/user/add</td>
    <td>login[string] password[string] email[string]</td>
    <td>render template for <b>login.html</b> with information otherwise render template <b>registration.html</b></td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/post</td>
    <td>image [image/png] content[string]</td>
    <td><b>Only for logged in users</b> goes to <b>/</b></td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/post</td>
    <td>image [image/png] content[string] title[string]</td>
    <td><b>Only for logged in users</b> goes to <b>/</b></td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/posts</td>
    <td>-</td>
    <td><b>Only for logged in users</b> returns user's posts[list of post] and username[string]</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/post/<int:post_id></td>
    <td>-</td>
    <td><b>Only for logged in users</b> returns user's post and username[string] if post exists otherwise returns 404</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/articles</td>
    <td>-</td>
    <td>returns articles[list of article] and author[string]</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/article/<int:post_id></td>
    <td>-</td>
    <td>returns article and author[string] if article exists otherwise returns 404</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/img/post/<int:article_id></td>
    <td>-</td>
    <td><b>Only for logged in users</b> returns post's image if post doesn't exist return 404</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/img/article/<int:article_id></td>
    <td>-</td>
    <td>image used in article if article doesn't exist return 404</td>
  </tr>
  <tr>
    <td>GET</td>
    <td>/guess</td>
    <td>-</td>
    <td><b>Only for logged in users</b> renders template for <b>guess.html</b></td>
  </tr>
  <tr>
    <td>POST</td>
    <td>/guess</td>
    <td>image[image/png]</td>
    <td><b>Only for logged in users</b> image/png which contains graph and average recognition accuracy</td>
  </tr>
</table>
## Usage of application:
For unregister user you can only see articles and read them.
For logged in users you can add a post (only for yourself), create an article and use guesserr.
In guesserr you just put a PNG image and wait for response from server.
Image in posts and articles are optional.
