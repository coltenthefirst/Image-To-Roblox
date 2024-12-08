export default function handler(req, res) {
  if (req.method === 'GET') {
    const htmlContent = `
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image To Roblox Parts Backend Processor</title>
        <link rel="icon" href="https://miro.medium.com/v2/resize:fit:512/1*nZ9VwHTLxAfNCuCjYAkajg.png" />
        <style>
          body {
            background-color: #000;
            color: #fff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
          }
          h1 {
            text-align: center;
            margin-top: 50px;
          }
          .content-container {
            text-align: center;
            padding: 20px;
            background-color: #333;
            margin: 20px auto;
            max-width: 600px;
            border-radius: 8px;
          }
        </style>
      </head>
      <body>
        <h1>Hello! You can't do nothing on this website unless you send a image to this link.</h1>
        <div class="content-container">
          <p>So, when you send a link of a image in roblox to this website. The website will download the image and run python code to make data, and it sends it back to roblox to make colored parts based on pixels of your images.</p>
        </div>
      </body>
      </html>
    `;

     Set response header to specify that it's HTML
    res.setHeader('Content-Type', 'text/html');
    res.status(200).send(htmlContent);
  } else {
    res.status(405).json({ error: 'Method Not Allowed' });
  }
}
