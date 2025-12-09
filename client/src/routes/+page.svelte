<script lang="ts">
  import emblaCarouselSvelte from "embla-carousel-svelte";
  import Autoplay, { type AutoplayType } from "embla-carousel-autoplay";
  import {
    Arrow_downward,
    Arrow_left,
    Arrow_right,
  } from "svelte-google-materialdesign-icons";
  import type { EmblaCarouselType, EmblaOptionsType } from "embla-carousel";
  import {
    ArcElement,
    Chart,
    Legend,
    PieController,
    Tooltip,
    BarController,
    LinearScale,
    CategoryScale,
    BarElement,
  } from "chart.js";

  import { onMount } from "svelte";
  import type { EmblaPluginType } from "embla-carousel";
  import Footer from "./footer.svelte";
  import type { HomePageData } from "$lib/types/homepage";
  import { API_URL } from "$lib/globals";

  export let data: HomePageData;

  const lastUpdated = "2025-09-17"; // Manually update this when needed
  const currentYear = new Date().getFullYear();

  // Custom rules for timeline animations
  let isTimelineShown = false;

  Chart.register(
    PieController,
    ArcElement,
    Legend,
    Tooltip,
    BarController,
    LinearScale,
    CategoryScale,
    BarElement,
  );

  // Small trick to pass the scroll container to the footer, we'll use [isMounted] to wait for the whole component to be mounted
  let isComponentMounted: boolean[] = [false];

  // My hobbies chart
  let hobbiesCanvas: HTMLCanvasElement;
  let knowledgeCanvas: HTMLCanvasElement;

  const knowledgeLabels = data.siteConfig.knowledge.map((k) => k.name);
  const knowledgeDatas = data.siteConfig.knowledge.map((k) => k.percent);

  const knowledgeChart = {
    labels: knowledgeLabels,
    data: knowledgeDatas,
  };

  // Timeline
  const events = data.siteConfig.timeline;

  const hobbiesLabels = data.siteConfig.hobbies.map((h) => h.name);
  const hobbiesDatas = data.siteConfig.hobbies.map((h) => h.percent);
  // Colors are hardcoded for now

  const hobbiesData = {
    // We will fetch this data from a JSON or so later
    labels: hobbiesLabels,
    datasets: [
      {
        data: hobbiesDatas,
        backgroundColor: [
          "rgba(100, 100, 100, 0.5)",
          "rgba(50, 50, 50, 0.5)",
          "rgba(255, 255, 255, 0.5)",
          "rgba(200, 200, 200, 0.5)",
        ],
        borderColor: [
          "rgba(100, 100, 100, 1)",
          "rgba(50, 50, 50, 1)",
          "rgba(255, 255, 255, 1)",
          "rgba(200, 200, 200, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  // Scroll to the last event in timeline
  let timelineDiv: HTMLDivElement;
  $: if (timelineDiv) {
    timelineDiv.scrollTo({ left: timelineDiv.scrollWidth, behavior: "smooth" });
  }

  // Embla Carousel
  let emblaApi: EmblaCarouselType;
  let options: EmblaOptionsType = { loop: true };
  let plugins: EmblaPluginType[] = [Autoplay()];

  function onInit(event: CustomEvent<EmblaCarouselType>) {
    emblaApi = event.detail;
  }

  // On Scroll Animations
  let onScrollElements: HTMLElement[] = [];
  let scrollPage: HTMLElement;
  function onScroll() {
    onScrollElements.forEach((el) => {
      const minScroll = el.dataset.minscroll
        ? parseInt(el.dataset.minscroll)
        : 100;
      const scrollTopPercent =
        ((scrollPage.scrollTop + scrollPage.clientHeight) /
          scrollPage.scrollHeight) *
        100;

      const currentOpacity = parseFloat(getComputedStyle(el).opacity); // Get the current opacity (better than dataset, which can lead to wired page state)

      if (
        scrollTopPercent >= minScroll &&
        !el.dataset.visible &&
        currentOpacity === 0
      ) {
        if (el.dataset.istimeline === "true") {
          isTimelineShown = true; // Trigger timeline animation
        }
        el.animate(
          [
            { opacity: 0, transform: "translateY(20px)" },
            { opacity: 1, transform: "translateY(0)" },
          ],
          {
            duration: 500,
            easing: "ease-in-out",
            fill: "forwards",
          },
        );
      } else if (scrollTopPercent < minScroll && currentOpacity === 1) {
        if (el.dataset.istimeline === "true") {
          isTimelineShown = false; // Trigger timeline animation
        }
        el.animate(
          [
            { opacity: 1, transform: "translateY(0)" },
            { opacity: 0, transform: "translateY(20px)" },
          ],
          {
            duration: 500,
            easing: "ease-in-out",
            fill: "forwards",
          },
        );
      }
    });
  }
  function addOnScrollElement(el: HTMLElement) {
    onScrollElements.push(el);
    onScrollElements = onScrollElements; // Refresh the classes
  }

  onMount(async () => {
    isComponentMounted[0] = true; // Trigger the footer to be mounted
    onScroll(); // Initial check
    new Chart(hobbiesCanvas, {
      type: "pie",
      data: hobbiesData,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "right",
            labels: {
              font: {
                family: "Source Code Pro",
              },
              color: "white",
            },
          },
        },
      },
    });
    new Chart(knowledgeCanvas, {
      type: "bar",
      data: {
        labels: knowledgeChart.labels,
        datasets: [
          {
            label: "Knowledge Level",
            data: knowledgeChart.data,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              font: {
                family: "Source Code Pro",
              },
              color: "white",
            },
          },
          x: {
            ticks: {
              font: {
                family: "Source Code Pro",
              },
              color: "white",
            },
          },
        },
        plugins: {
          legend: {
            display: true,
            labels: {
              font: {
                family: "Source Code Pro",
              },
              color: "white",
            },
          },
        },
        backgroundColor: "rgba(100, 100, 100, 0.5)",
        borderColor: "black",
      },
    });
  });
</script>

<div class="scrollablePage" onscroll={onScroll} bind:this={scrollPage}>
  <header class="bg-img">
    <div class="text">
      <h1><span>WebDash</span></h1>
      <h2>Explore my projects as a 2nd-year IT student.</h2>
    </div>
    <div class="scroll">
      <button
        class="nostyle"
        onclick={() => {
          scrollPage?.scrollTo({ top: window.innerHeight, behavior: "smooth" });
        }}
      >
        <div class="noevents">
          <Arrow_downward variation="round" size="100" />
        </div>
      </button>
    </div>
  </header>
  <main>
    <section class="section-type2" id="whoami">
      <h2>Who am I?</h2>
      <div use:addOnScrollElement class="_onscrolldata" data-minScroll="35">
        <p class="p_1">
          {@html data.siteConfig.whoami.text1}
          <!-- Allow HTML, because I'm the only one that can edit this -->
        </p>
        <p class="p_2">
          {@html data.siteConfig.whoami.text2}
        </p>
      </div>
    </section>
    <section class="section-type1">
      <h2>Projects...</h2>
      <div use:addOnScrollElement class="_onscrolldata" data-minScroll="55">
        <div
          class="embla"
          use:emblaCarouselSvelte={{ options, plugins }}
          onemblaInit={onInit}
        >
          <div class="embla__container">
            {#each data.siteConfig.projects as project}
              <div
                class="embla__slide proj-img bg-img"
                style="background-image: url('{API_URL}/site/images/{project.img}');"
              >
                <div class="texts">
                  <h3>{project.name}</h3>
                  <p>
                    {project.desc}
                    <a href={project.url}>View Project</a>
                  </p>
                </div>
              </div>
            {/each}
          </div>
        </div>
        <button onclick={() => emblaApi.scrollPrev()}>Prev</button>
        <button onclick={() => emblaApi.scrollNext()}>Next</button>
      </div>
    </section>
    <section class="section-type2">
      <div
        class="_onscrolldata chartContainer right"
        use:addOnScrollElement
        data-minScroll="70"
      >
        <h2>Hobbies</h2>
        <canvas id="hobbies" width="300" height="300" bind:this={hobbiesCanvas}
        ></canvas>
      </div>
      <div class="sep"></div>
      <div class="knowledgeContainer">
        <div
          class="_onscrolldata chartContainer"
          use:addOnScrollElement
          data-minScroll="80"
        >
          <h2>Knowledge</h2>
          <canvas
            id="knowledge"
            width="300"
            height="300"
            bind:this={knowledgeCanvas}
          ></canvas>
        </div>
        <div>
          <p>Last updated: {lastUpdated}.</p>
          <h6>These are an estimation. They might not be accurate.</h6>
        </div>
      </div>
    </section>
    <section class="section-type1">
      <div
        class="_onscrolldata"
        data-isTimeline="true"
        use:addOnScrollElement
        data-minScroll="90"
      >
        <h1>My timeline</h1>
        <div class="timeline" bind:this={timelineDiv}>
          <div class="events">
            {#each events as event}
              <div
                class="eventbar"
                class:rotate={isTimelineShown}
                style="left: {((event.year - events[0].year) /
                  (currentYear - events[0].year)) *
                  100}%"
              >
                <div class="event-text">
                  <div class="event-year">{event.year}</div>
                  <div class="event_name">{event.event}</div>
                </div>
              </div>
            {/each}
          </div>
          <div class="timeline-bar"></div>
        </div>
      </div>
    </section>
  </main>
  <Footer
    scrollContainer={scrollPage}
    isMounted={isComponentMounted}
    data={data.siteConfig.general_footer}
  />
</div>

<style>
  a {
    color: var(--text-primary);
    text-decoration: underline;
    transition: 0.3s;
  }
  .scrollablePage {
    overflow: scroll;
    width: 100%;
    height: 100vh;
    scrollbar-width: none;
  }

  h1,
  h2 {
    margin: 0;
    padding: 0.25em;
  }

  header {
    left: 0;
    top: 0;
    width: 100%;
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    background-image: url("/images/_homepage/header.webp");
    color: var(--text-primary);
    image-rendering: auto;
    backface-visibility: hidden;
    height: 100vh;
    background-position: 50% 70%; /* Adjusted */
    position: relative;
    animation: backgroundAnim 20s ease-in-out infinite alternate;
  }

  header .text {
    border: 2px solid var(--border-primary);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    background-color: var(--bg-primary);
    color: var(--text-secondary);
    padding: 40px;
    border-radius: 20px;
    color: var(--text-secondary);
  }

  header .scroll {
    position: absolute;
    user-select: none;
    cursor: pointer;
    z-index: -1; /* Ensure it's behind other content */
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 10em;
    color: var(--text-primary);
    animation: scrollAnim 2s ease-in-out infinite;
    transition: 0.5s;
    stroke: none;
  }

  header .scroll:hover {
    transform: translateX(-50%) scale(1.1);
  }

  header .text h1 span {
    animation: h1TextAnim 1s ease-in-out forwards 1s;
    opacity: 0;
    display: inline-block;
    height: 0;
    color: var(--text-inverted);
  }

  header .text h1 {
    left: 0;
    width: 10%;
    background-color: var(--bg-inverted);
    border-radius: 20px;
    animation: h1AfterAnim 1s ease-in-out forwards;
  }

  .section-type2 {
    border: 2px solid var(--border-primary);
    background-color: var(--bg-secondary);
    color: var(--text-primary);
    color: var(--text-primary);
    padding: 20px;
    text-align: center;
  }

  .section-type1 {
    border: 2px solid var(--border-secondary);
    background-color: var(--bg-primary);
    color: var(--text-secondary);
    color: var(--text-primary);
    padding: 20px;
    text-align: center;
  }

  ._onscrolldata {
    opacity: 0;
  }

  ._onscrolldata p {
    max-width: 800px;
    text-align: justify;
  }

  button.nostyle {
    all: unset;
    cursor: pointer;
  }

  button:not(.nostyle) {
    background-color: var(--bg-button);
    color: var(--text-primary);
    border: none;
    padding: 10px 20px;
    margin: 10px;
    border-radius: 10px;
    cursor: pointer;
    position: relative;
    transition: 0.3s;
  }

  button:not(.nostyle):hover {
    color: var(--text-primary);
    padding-left: 25px;
  }

  button:not(.nostyle):active {
    border-radius: 15px;
  }

  ._onscrolldata .p_1 {
    margin: 0 10%;
  }

  ._onscrolldata .p_2 {
    text-align: left;
    margin: 5% 80%;
    width: 20%;
  }

  .embla {
    overflow: hidden;
    margin: auto;
    border: 2px solid white;
    border-radius: 20px;
    max-width: 75%;
    height: 300px;
  }
  .embla__container {
    display: flex;
  }
  .embla__slide {
    flex: 0 0 100%;
    min-width: 0;
    min-height: 300px;
    position: relative;
  }

  .embla__slide .texts {
    position: absolute;
    bottom: 20px;
    left: 20px;
    color: var(--text-secondary);
    text-align: left;
    background-color: #000000bb;
    padding: 20px;
    border-radius: 10px;
    max-width: 60%;
  }

  .proj-img {
    background-size: cover;
    background-position: center;
    width: 100%;
  }

  .chartContainer {
    width: 325px;
    height: 350px;
    margin: auto;
  }

  .right {
    margin-right: 35%;
  }

  .sep {
    margin-bottom: 30px;
    position: relative;
  }

  .sep::after {
    content: "";
    width: 80%;
    height: 4px;
    background-color: gray;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 20px;
  }

  .knowledgeContainer {
    display: flex;
    justify-content: space-between;
  }

  .timeline {
    position: relative;
    width: 100%;
    color: var(--text-secondary);
    height: 200px;
    font-size: 70%;
  }

  .timeline .timeline-bar {
    width: 100%;
    height: 10px;
    position: absolute;
    background-color: var(--border-primary);
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    border-radius: 20px;
  }

  .timeline .eventbar {
    width: 100px;
    height: 5px;
    position: absolute;
    background-color: var(--border-primary);
    top: 50%;
    transition: 0.5s;
    animation: toRotateReverse 1s ease-in-out forwards;
  }

  .timeline .eventbar.rotate {
    animation: toRotate 1s ease-in-out forwards;
  }

  .timeline .event-text {
    transform: translateY(-100%);
  }

  .timeline .event-text .event-year {
    font-size: 150%;
  }

  .noevents {
    pointer-events: none;
  }

  @keyframes toRotateReverse {
    from {
      transform: rotate(-45deg) translateX(50px);
    }
    to {
      transform: rotate(0deg) translateX(50px);
    }
  }

  @keyframes toRotate {
    from {
      transform: rotate(0deg) translateX(50px);
    }
    to {
      transform: rotate(-45deg) translateX(50px);
    }
  }

  @keyframes backgroundAnim {
    from {
      background-size: 100%;
    }
    to {
      background-size: 130%;
    }
  }

  @keyframes scrollAnim {
    0%,
    100% {
      transform: translateX(-50%) translateY(0);
    }
    50% {
      transform: translateX(-50%) translateY(20px);
    }
  }

  @keyframes h1TextAnim {
    from {
      opacity: 0;
      height: 0;
    }
    to {
      opacity: 1;
      height: 100%;
    }
  }

  @keyframes h1AfterAnim {
    0% {
      width: 10%;
      transform: scaleY(0.1);
    }
    50% {
      width: 100%;
      transform: scaleY(0.1);
    }
    100% {
      width: 100%;
      transform: scaleY(1);
    }
  }

  @media screen and (max-width: 1000px) {
    header {
      background-size: cover !important;
    }

    #whoami .p_2 {
      margin: 5% 50%;
      width: 50%;
    }

    .chartContainer {
      width: 90%;
    }

    .knowledgeContainer {
      flex-direction: column;
      align-items: center;
    }

    .timeline {
      overflow: scroll;
      scrollbar-width: none;
    }

    .timeline .timeline-bar {
      width: 1000px;
      left: 0;
      transform: translateY(-50%);
    }

    .timeline .events {
      width: 1000px;
      height: 200px;
      position: relative;
    }
  }

  @media screen and (max-height: 650px) {
    .scroll {
      display: none;
    }
  }
</style>
