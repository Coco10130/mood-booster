async function fetchData(
  url,
  containerId,
  createContent,
  manageLoading = true
) {
  const container = document.getElementById(containerId);
  const loading = document.getElementById("loading");

  try {
    if (manageLoading) loading.style.display = "flex";
    container.innerHTML = "";

    const response = await fetch(url);
    if (!response.ok) throw new Error("Network response was not ok");
    const data = await response.json();

    container.innerHTML = "";
    data.forEach((item) => container.appendChild(createContent(item)));
  } catch (error) {
    console.error("Fetch error:", error);
    container.innerHTML = `
      <div class="error-message">
          <p>Failed to load content. Please try again!</p>
      </div>`;
  } finally {
    if (manageLoading) loading.style.display = "none";
  }
}

// Content creation functions
const createCatFactContent = (fact) => {
  const div = document.createElement("div");
  div.className = "content-item";
  div.innerHTML = `
    <div class="fact-card">
        <p class="fact-text">${fact.fact}</p>
        
    </div>`;
  return div;
};

const createDogImageContent = (dog) => {
  const div = document.createElement("div");
  div.className = "content-item";
  div.innerHTML = `
    <div class="image-card">
        <div class="image-wrapper">
            <img src="${dog.message}" alt="Cute Dog" class="dog-image">
        </div>
        
    </div>`;
  return div;
};

const createJokeContent = (joke) => {
  const div = document.createElement("div");
  div.className = "content-item";
  let jokeHTML = '<div class="joke-card">';

  if (joke.type === "twopart") {
    jokeHTML += `<p class="setup">${joke.setup}</p><p class="punchline">${joke.punchline}</p>`;
  } else {
    jokeHTML += `<p class="single-joke">${joke.joke || "No joke found"}</p>`;
  }

  div.innerHTML = jokeHTML;
  return div;
};

// Event listeners
document.getElementById("getCatFacts").addEventListener("click", () => {
  const length = document.getElementById("catFactLength").value;
  if (length > 0) {
    console.log(length);
    fetchData(
      `/api/cat/random/${length}`,
      "catFactsContainer",
      createCatFactContent
    );
  }
  fetchData("/api/cat/random", "catFactsContainer", createCatFactContent);
});

document.getElementById("getDogImages").addEventListener("click", () => {
  fetchData("/api/dog/random", "dogImagesContainer", createDogImageContent);
});

document.getElementById("getJokes").addEventListener("click", () => {
  const selectedCategory = document.querySelector(
    'input[name="jokeCategory"]:checked'
  ).value;

  if (selectedCategory === "Any") {
    fetchData("/api/joke/random", "jokesContainer", createJokeContent);
  } else {
    const apiUrl = `/api/joke/random/${selectedCategory}`;
    fetchData(apiUrl, "jokesContainer", createJokeContent);
  }
});

document.getElementById("moodBooster").addEventListener("click", async () => {
  const loading = document.getElementById("loading");
  try {
    loading.style.display = "flex";
    await Promise.all([
      fetchData(
        "/api/cat/random",
        "catFactsContainer",
        createCatFactContent,
        false
      ),
      fetchData(
        "/api/dog/random",
        "dogImagesContainer",
        createDogImageContent,
        false
      ),
      fetchData("/api/joke/random", "jokesContainer", createJokeContent, false),
    ]);
  } catch (error) {
    console.error("Mood booster error:", error);
  } finally {
    loading.style.display = "none";
  }
});

document.getElementById("theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
});

// Favorite Saving Function
