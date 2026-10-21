    // Chapter 1's progressive comparison. Works offline on the lesson and
    // standalone review page; no model, account or host API is involved.
    (() => {
      const root = document.getElementById('salmon-workflow-guided');
      if (!root) return;
      root.replaceChildren();
      root.append(el('h3', 'workflow-heading', 'Less detective work. More time for the biology.'));
      const controls = el('div', 'tour-controls');
      controls.setAttribute('role', 'group');
      controls.setAttribute('aria-label', 'Workflow timeline controls');
      [['back', 'Previous'], ['next', 'Next'], ['play', 'Play'], ['full', 'Full diagram']].forEach(([id, label]) => {
        const button = el('button', 'btn btn-sm ' + (id === 'next' ? 'btn-primary' : 'btn-outline-secondary'), label);
        button.id = 'salmon-tour-' + id;
        button.type = 'button';
        if (id === 'full' || id === 'play') button.setAttribute('aria-pressed', 'false');
        controls.append(button);
      });
      root.append(controls);
      const progress = el('div', 'tour-position');
      progress.id = 'salmon-tour-position';
      progress.setAttribute('aria-live', 'polite');
      root.append(progress);
      const figure = el('figure');
      figure.setAttribute('aria-label', 'Two routes from the same CU-year question to reusable data');
      const board = el('div', 'canvas');
      board.id = 'salmon-tour-canvas';
      const lines = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      lines.classList.add('lines');
      lines.setAttribute('aria-hidden', 'true');
      board.append(lines, el('div', 'question', 'Assemble the best available annual spawner estimates by Conservation Unit.'));
      const laneHeadings = el('div', 'lane-headings');
      [['The usual route', 'Files and scattered explanations'], ['With reviewed Salmon Data Packages', 'Meanings and evidence travel with the data']].forEach(([title, note]) => {
        const heading = el('div', 'lane-heading', title);
        heading.append(el('span', 'text-small', note));
        laneHeadings.append(heading);
      });
      board.append(laneHeadings);
      const stageContainer = el('div');
      stageContainer.id = 'salmon-tour-stages';
      board.append(stageContainer);
      figure.append(board);
      const evidenceCaption = el('figcaption', 'text-small');
      evidenceCaption.id = 'salmon-tour-caption';
      figure.append(evidenceCaption);
      root.append(figure);
      const evidenceLinks = el('div', 'source-links text-small');
      evidenceLinks.id = 'salmon-tour-sources';
      const siteRoot = root.dataset.siteRoot || '';
      [['Yukon excerpt', 'files/intro-comparison/yukon-excerpt.csv'], ['Fraser excerpt', 'files/intro-comparison/fraser-excerpt.csv'], ['Compare the source evidence', 'session-1.html#the-archetypical-data-problem']].forEach(([label, href]) => {
        const link = el('a', '', label);
        link.href = siteRoot + href;
        evidenceLinks.append(link);
      });
      root.append(evidenceLinks);
      const announcement = el('div', 'visually-hidden');
      announcement.id = 'salmon-tour-status';
      announcement.setAttribute('aria-live', 'polite');
      root.append(announcement);
      const canvas = root.querySelector('#salmon-tour-canvas');
      const stageRoot = root.querySelector('#salmon-tour-stages');
      const svg = root.querySelector('.lines');
      const back = root.querySelector('#salmon-tour-back');
      const next = root.querySelector('#salmon-tour-next');
      const play = root.querySelector('#salmon-tour-play');
      const full = root.querySelector('#salmon-tour-full');
      const position = root.querySelector('#salmon-tour-position');
      const status = root.querySelector('#salmon-tour-status');
      const sources = root.querySelector('#salmon-tour-sources');
      const caption = root.querySelector('#salmon-tour-caption');
      const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
      const NS = 'http://www.w3.org/2000/svg';
      const part = (label, note = '') => ({label, note});
      const node = (id, label, note, detail, verdict = null) => ({id, label, note, detail, verdict});

      const stages = [
        {
          title: 'Find and understand the data',
          left: [
            node('collect', 'Find and obtain the files', 'Downloads, access requests and different formats.', [
              part('Find candidate datasets', 'Yukon and Fraser sources for annual abundance'),
              part('Obtain files and permissions', 'A download may still leave missing context')
            ]),
            node('documents', 'Search papers and appendices', 'Which methods describe these columns?', [
              part('Read the methods'),
              part('Match the prose to a column', 'Quantity, scope, year and uncertainty may remain unclear')
            ]),
            node('provider', 'Ask, wait and ask again', 'An unavailable author can leave an assumption unresolved.', [
              part('Email the provider', 'A contact may have moved or retired'),
              part('Clarify what the value represents'),
              part('Return to the methods', 'A partial answer can raise another question')
            ])
          ],
          right: [
            node('packages', 'Open reviewed data packages', 'Data, meanings, methods and source links together.', [
              part('Salmon Data Package', 'A common structure for data and their descriptions'),
              part('Salmon Domain Ontology', 'Maintained definitions to compare with the data'),
              part('Starting with raw files?', 'Draw → dictionary → provider or peer review'),
              part('Build the first package with metasalmon', 'Preserve that preparation for later users')
            ])
          ],
          loop: ['provider', 'documents']
        },
        {
          title: 'Check and combine the estimates',
          left: [
            node('reshape', 'Standardize each table', 'Reshape fields, identifiers, codes and units.', [
              part('Write an import for each format'),
              part('Resolve column and code meanings'),
              part('Record transformations', 'A change in format must preserve the source values')
            ]),
            node('join-manual', 'Join, then revisit the meanings', 'New mismatches send you back to the evidence.', [
              part('Find the abundance candidates', 'Yukon mean and Fraser SpnForAbd_Total'),
              part('Check CU, year, scope and methods', 'These records concern different CUs; retain their identities'),
              part('Return to the source for gaps', 'Shared labels alone do not establish comparability')
            ])
          ],
          right: [
            node('join-reviewed', 'Review fit and integrate', 'A common format and explicit meanings support repeatable code.', [
              part('Locate the candidate fields', 'Descriptions identify Yukon mean and Fraser SpnForAbd_Total as candidates'),
              part('Check fit for the research question', 'A person reviews scope, methods and uncertainty'),
              part('Run explicit mappings and study code', 'metasalmon supports the packages; the analysis still needs its own code'),
              part('Keep the CU-year records and their differences', 'Retain each source identity, method, scope and uncertainty')
            ])
          ]
        },
        {
          title: 'Draw a conclusion the evidence supports',
          left: [
            node('claim-risk', 'Analyse with an unchecked interpretation', '“High confidence” is read as precise abundance.', [
              part('Fraser 2023: ConfidenceRating = High', 'The same record reports SpnForAbd_Total = 146371'),
              part('Assume it describes abundance precision'),
              part('Make an unsupported precision claim', 'The field definition actually concerns assessment status')
            ], {tone:'caution', label:'Potentially wrong assumption', note:'A plausible label can lead to an unsupported conclusion.'})
          ],
          right: [
            node('claim-checked', 'Analyse with the meaning checked', 'Status confidence and abundance uncertainty stay distinct.', [
              part('Read the Fraser field definition', 'ConfidenceRating describes the assessment status'),
              part('Keep Yukon estimate uncertainty separate', 'Yukon lower and upper concern the reconstruction estimate; check their definition in the methods'),
              part('Make the supported statement', 'This status rating does not establish abundance precision')
            ], {tone:'checked', label:'Interpretation checked against evidence', note:'This mistaken inference is caught before the conclusion.'})
          ]
        },
        {
          title: 'Publish once, help the next project',
          left: [
            node('rebuild', 'Reconstruct metadata at the end', 'The paper is ready; the data publication still needs work.', [
              part('Find the source and processing history'),
              part('Choose a metadata structure'),
              part('Write descriptions and code meanings', 'Important answers may still be in old emails')
            ]),
            node('publish-late', 'Prepare and publish the data', 'Incomplete explanations leave work for the next team.', [
              part('Review rights, credit and metadata'),
              part('Deposit and release the dataset'),
              part('Answer the next user’s questions', 'The clarification work may be repeated')
            ])
          ],
          right: [
            node('publish-ready', 'Validate, publish and pass it on', 'The reviewed explanation is already part of the package.', [
              part('Review rights, credit and final metadata', 'Recognize the source providers and standardization work'),
              part('Validate and upload with metasalmon', 'Prepare the package and EML for KNB'),
              part('Release through the repository', 'KNB publication and DOI are a separate action'),
              part('Reuse packages and maintained meanings', 'Keep source and derived data traceable'),
              part('Contribute the missing meanings', 'Local vocabulary or model, an evidenced bridge, or a shared-term request')
            ])
          ],
          result: ['Next team: repeat the detective work', 'Next team: start with more of the work done']
        }
      ];

      let stageIndex = 0;
      let showFull = false;
      let expanded = new Set();
      let playing = false;
      let timer = 0;
      let frame = 0;
      let animateNext = false;

      function el(tag, className, text) {
        const item = document.createElement(tag);
        if (className) item.className = className;
        if (text) item.textContent = text;
        return item;
      }

      function stopPlayback() {
        playing = false;
        clearTimeout(timer);
        play.textContent = stageIndex === 3 && !showFull ? 'Replay' : 'Play';
        play.setAttribute('aria-pressed', 'false');
      }

      function scheduleAdvance() {
        clearTimeout(timer);
        if (!playing) return;
        timer = window.setTimeout(() => {
          if (stageIndex === 3) {
            stopPlayback();
            return;
          }
          stageIndex += 1;
          render(true);
          scheduleAdvance();
        }, 7000);
      }

      function buildNode(item, laneNumber) {
        const open = expanded.has(item.id);
        const container = el('div', 'node');
        container.dataset.node = item.id;
        container.dataset.lane = laneNumber;
        if (open) container.dataset.expanded = 'true';
        const label = item.label + (open ? ' −' : ' +');
        const button = el('button', 'btn btn-sm btn-outline-secondary', label);
        button.type = 'button';
        button.dataset.label = label;
        button.setAttribute('aria-label', label);
        button.setAttribute('aria-expanded', String(open));
        button.setAttribute('aria-controls', 'guided-detail-' + item.id);
        button.addEventListener('click', () => {
          stopPlayback();
          if (expanded.has(item.id)) expanded.delete(item.id); else expanded.add(item.id);
          render(true);
          stageRoot.querySelector('[data-node="' + item.id + '"] button').focus({preventScroll:true});
          status.textContent = item.label + ': ' + (expanded.has(item.id) ? 'detail opened within the diagram' : 'detail closed');
        });
        container.append(button, el('div', 'node-caption text-small', item.note));
        if (item.verdict) {
          const verdict = el('div', 'verdict');
          verdict.dataset.tone = item.verdict.tone;
          const symbol = el('span', 'symbol');
          symbol.textContent = item.verdict.tone === 'checked' ? '✓' : '⚠';
          symbol.setAttribute('aria-hidden', 'true');
          verdict.append(symbol, el('div', 'verdict-label', item.verdict.label), el('div', 'text-small', item.verdict.note));
          container.append(verdict);
        }
        const nested = el('div', 'nested');
        nested.id = 'guided-detail-' + item.id;
        nested.hidden = !open;
        item.detail.forEach(detail => {
          const itemNode = el('div', 'nested-node');
          itemNode.append(el('strong', '', detail.label));
          if (detail.note) itemNode.append(el('span', 'text-small', detail.note));
          nested.append(itemNode);
        });
        container.append(nested);
        return container;
      }

      function render(animate = false) {
        back.disabled = showFull || stageIndex === 0;
        next.disabled = showFull || stageIndex === 3;
        full.setAttribute('aria-pressed', String(showFull));
        full.textContent = showFull ? 'Return to tour' : 'Full diagram';
        play.textContent = playing ? 'Pause' : stageIndex === 3 && !showFull ? 'Replay' : 'Play';
        play.setAttribute('aria-pressed', String(playing));
        position.textContent = showFull ? 'Whole project · fewer repeated preparation tasks' : (stageIndex + 1) + ' of 4 · ' + stages[stageIndex].title;
        stageRoot.replaceChildren();
        const visibleStages = showFull ? stages : stages.slice(0, stageIndex + 1);
        visibleStages.forEach(stage => {
          const section = el('div', 'stage');
          section.dataset.stage = stages.indexOf(stage);
          const stageHeader = el('div', 'stage-header');
          const stageHeading = el('div', 'stage-heading');
          stageHeading.append(el('span', 'phase-number', 'Phase ' + (stages.indexOf(stage) + 1)), el('h4', 'stage-title', stage.title));
          stageHeader.append(el('hr'), stageHeading, el('hr'));
          section.append(stageHeader);
          const columns = el('div', 'stage-columns');
          [stage.left, stage.right].forEach((items, laneNumber) => {
            const lane = el('div', 'lane');
            lane.dataset.lane = laneNumber;
            items.forEach(item => lane.append(buildNode(item, laneNumber)));
            if (stage.result) lane.append(el('div', 'reuse-result text-small', stage.result[laneNumber]));
            columns.append(lane);
          });
          section.append(columns);
          stageRoot.append(section);
        });
        const showEvidence = showFull || stageIndex >= 2;
        sources.hidden = !showEvidence;
        caption.hidden = !showEvidence;
        caption.textContent = showEvidence
          ? 'The confidence example is a teaching counterfactual using real fields, not an error attributed to the source authors. Spacing does not measure time.'
          : '';
        if (showFull || stageIndex === 3) caption.textContent += ' The workshop uses KNB test; the expanded publication steps illustrate a later production route.';
        animateNext = animate && !motion.matches;
        requestDraw();
      }

      function svgEl(tag, attributes) {
        const item = document.createElementNS(NS, tag);
        Object.entries(attributes || {}).forEach(([key,value]) => item.setAttribute(key, String(value)));
        return item;
      }

      function rectOf(item, origin) {
        const b = item.getBoundingClientRect();
        return {x:b.left-origin.left,y:b.top-origin.top,w:b.width,h:b.height,cx:b.left-origin.left+b.width/2,bottom:b.bottom-origin.top};
      }

      function connect(d, type) {
        const edge = svgEl('path', {d,class:type+'-line','marker-end':'url(#guided-arrow-'+type+')'});
        svg.append(edge);
        return edge;
      }

      function wrapLabels() {
        const limit = Math.max(9, Math.min(33, Math.floor(((canvas.clientWidth - 70) / 2 - 46) / 7.5)));
        stageRoot.querySelectorAll('button').forEach(button => {
          if (button.dataset.wrap === String(limit)) return;
          button.dataset.wrap = String(limit);
          const label = el('span');
          let line = '';
          button.dataset.label.replace(/ ([+−])$/, '\u00a0$1').split(' ').forEach(word => {
            if (line && (line+' '+word).length > limit) {
              label.append(document.createTextNode(line), document.createElement('br'));
              line = word;
            } else line += (line ? ' ' : '') + word;
          });
          label.append(document.createTextNode(line));
          button.replaceChildren(label);
        });
      }

      function draw() {
        wrapLabels();
        const origin = canvas.getBoundingClientRect();
        const previousEdges = new Set([...svg.querySelectorAll('path[class$="-line"]')].map(edge => edge.getAttribute('class') + ':' + edge.getAttribute('d')));
        svg.setAttribute('width', origin.width);
        svg.setAttribute('height', origin.height);
        svg.setAttribute('viewBox', '0 0 '+origin.width+' '+origin.height);
        svg.replaceChildren();
        const defs = svgEl('defs');
        [['usual','var(--muted-foreground)'],['package','var(--viz-series-1)'],['loop','var(--orange)']].forEach(([name,color]) => {
          const arrow = svgEl('marker',{id:'guided-arrow-'+name,viewBox:'0 0 8 8',refX:7,refY:4,markerWidth:6,markerHeight:6,orient:'auto'});
          arrow.append(svgEl('path',{d:'M 1 1 L 7 4 L 1 7',fill:'none',stroke:color,'stroke-width':1.5}));
          defs.append(arrow);
        });
        svg.append(defs);
        const question = rectOf(root.querySelector('.question'), origin);
        const headings = [...root.querySelectorAll('.lane-heading')].map(item => rectOf(item, origin));
        const lanes = [0,1].map(n => [...stageRoot.querySelectorAll('.node[data-lane="'+n+'"]')]);
        const phaseBands = [...stageRoot.querySelectorAll('.stage-header')].map(item => rectOf(item, origin));

        // Leave a clear band around each phase heading as the timeline extends.
        function connectTimeline(x, start, end, type) {
          let cursor = start;
          const segments = [];
          phaseBands.forEach(band => {
            if (band.bottom + 6 <= cursor || band.y - 6 >= end) return;
            if (band.y - 6 > cursor) segments.push('M ' + x + ' ' + cursor + ' V ' + (band.y - 6));
            cursor = Math.min(end, band.bottom + 6);
          });
          if (cursor < end) segments.push('M ' + x + ' ' + cursor + ' V ' + end);
          if (segments.length) connect(segments.join(' '), type);
        }

        lanes.forEach((nodes, laneNumber) => {
          const type = laneNumber ? 'package' : 'usual';
          const heading = headings[laneNumber];
          const first = rectOf(nodes[0],origin);
          connect('M '+question.cx+' '+question.bottom+' V '+(question.bottom+11)+' H '+heading.cx+' V '+(heading.y-5),type);
          connectTimeline(heading.cx, heading.bottom + 5, first.y - 5, type);
          nodes.forEach((item,index) => {
            const b = rectOf(item,origin);
            if (item.dataset.expanded) {
              svg.append(svgEl('rect',{x:b.x,y:b.y,width:b.w,height:b.h,rx:8,class:'group-box'}));
              const parts = [...item.querySelectorAll('.nested-node')].map(n => rectOf(n,origin));
              parts.forEach(p => svg.append(svgEl('rect',{x:p.x,y:p.y,width:p.w,height:p.h,rx:6,class:'detail-box'})));
              for (let i=0;i<parts.length-1;i++) connect('M '+parts[i].cx+' '+(parts[i].bottom+2)+' V '+(parts[i+1].y-4),type);
            }
            if (index < nodes.length-1) {
              const destination = rectOf(nodes[index+1],origin);
              connectTimeline(b.cx, b.bottom + 2, destination.y - 5, type);
            }
          });
        });

        function anchor(id) {
          const item = stageRoot.querySelector('[data-node="'+id+'"]');
          if (!item) return null;
          return rectOf(item.dataset.expanded ? item : item.querySelector('button'),origin);
        }
        function loop(from,to) {
          const a = anchor(from), b = anchor(to);
          if (!a || !b) return;
          const outer = Math.max(2,Math.min(a.x,b.x)-15);
          connect('M '+(a.x-2)+' '+(a.y+Math.min(a.h/2,22))+' H '+outer+' V '+(b.y+Math.min(b.h/2,22))+' H '+(b.x-3),'loop');
        }
        loop('provider','documents');
        loop('join-manual','documents');

        if (animateNext && !motion.matches) {
          svg.querySelectorAll('path[class$="-line"]').forEach(edge => {
            if (previousEdges.has(edge.getAttribute('class') + ':' + edge.getAttribute('d'))) return;
            const length = edge.getTotalLength();
            if (length > 0) edge.animate([{strokeDasharray:length,strokeDashoffset:length},{strokeDasharray:length,strokeDashoffset:0}],{duration:650,easing:'ease-out'});
          });
        }
        animateNext = false;
      }

      function requestDraw() {
        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(draw);
      }
      back.addEventListener('click', () => {
        stopPlayback(); stageIndex = Math.max(0,stageIndex-1); render(true);
      });
      next.addEventListener('click', () => {
        stopPlayback(); stageIndex = Math.min(3,stageIndex+1); render(true);
      });
      full.addEventListener('click', () => {
        stopPlayback(); showFull = !showFull; render(true);
      });
      play.addEventListener('click', () => {
        if (playing) {stopPlayback(); return;}
        if (showFull || stageIndex === 3) stageIndex = 0;
        showFull = false;
        expanded.clear();
        playing = true;
        render(true); scheduleAdvance();
      });
      document.addEventListener('visibilitychange', () => {if (document.hidden) stopPlayback();});
      new ResizeObserver(requestDraw).observe(canvas);
      render();
    })();
