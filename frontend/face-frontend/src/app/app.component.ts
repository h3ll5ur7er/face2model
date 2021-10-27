import { HttpClient } from '@angular/common/http';
import { Component, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import * as THREE from 'three';
import { PLYLoader } from 'three/examples/jsm/loaders/PLYLoader';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  title = 'face-frontend';
  @ViewChild('3dContext') container: ElementRef<HTMLDivElement>;
  // image: File = undefined;
  texture: any;

  cameraAngle = [0, 0];
  cameraAngleTarget = [0, 0];
  camera: THREE.PerspectiveCamera;
  scene: THREE.Scene;
  renderer: THREE.WebGLRenderer;

  mouseX = 0;
  mouseY = 0;

  windowHalfX = window.innerWidth / 2;
  windowHalfY = window.innerHeight / 4;

  object: THREE.BufferGeometry;

  constructor(private http: HttpClient) {}
  ngAfterViewInit(): void {
    this.init('face.jpg.ply');
    this.animate();
  }

  load(filename: string): void {
    this.init(filename);
    this.animate();
  }

  loadModel(): void {
    console.log(this.object);
    const material = new THREE.MeshBasicMaterial( { wireframe: false, vertexColors: true } );
    const mesh = new THREE.Mesh(this.object, material);
    mesh.position.set(100, 100, 0);
    mesh.rotateZ(Math.PI);
    // mesh.rotateY(Math.PI);
    this.scene.add( mesh );
  }
  onProgress( xhr ): void { }
  onError(): void {}
  init(filename: string): void {
    this.camera = new THREE.PerspectiveCamera( 45, window.innerWidth / (window.innerHeight / 2), 1, 2000 );
    this.camera.position.z = 250;

    this.scene = new THREE.Scene();

    const ambientLight = new THREE.AmbientLight( 0xcccccc, 0.4 );
    this.scene.add( ambientLight );

    const pointLight = new THREE.PointLight( 0xffffff, 0.8 );
    this.camera.add( pointLight );
    this.scene.add( this.camera );

    const manager = new THREE.LoadingManager( () => this.loadModel() );

    manager.onProgress = ( item, loaded, total ) => console.log( item, loaded, total );

    const loader = new PLYLoader( manager );
    loader.load( 'data/' + filename, ( obj ) => this.object = obj, (xhr) => this.onProgress(xhr), () => this.onError() );

    this.renderer = new THREE.WebGLRenderer();
    this.renderer.setPixelRatio( window.devicePixelRatio );
    this.renderer.setSize( window.innerWidth, window.innerHeight / 2);
    this.container.nativeElement.appendChild( this.renderer.domElement );
    document.addEventListener( 'mousemove', (evt) => this.onDocumentMouseMove(evt) );
    window.addEventListener( 'resize', () => this.onWindowResize() );
  }

  onWindowResize(): void {
    this.windowHalfX = window.innerWidth / 2;
    this.windowHalfY = window.innerHeight / 4;
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize( window.innerWidth, window.innerHeight / 2 );
  }

  onDocumentMouseMove( event: MouseEvent ): void {
    const angle = 270;
    this.mouseX = ( event.offsetX / (this.windowHalfX * 2) ) - .5 ;
    this.mouseY = ( event.offsetY / (this.windowHalfY * 4) ) - .5 ;
    this.cameraAngleTarget = [this.mouseX * angle, this.mouseY * angle];
  }

  animate(): void {
    requestAnimationFrame( () => this.animate() );
    this.render();
  }

  render(): void {
    this.cameraAngle[0] += (this.cameraAngleTarget[0] - this.cameraAngle[0]) * 0.05;
    this.cameraAngle[1] += (this.cameraAngleTarget[1] - this.cameraAngle[1]) * 0.05;
    this.camera.position.x = Math.sin(-this.cameraAngle[0] * Math.PI / 180) * 200;
    this.camera.position.y = Math.cos(this.cameraAngle[1] * Math.PI / 180) * 200;




    // this.camera.position.x += ( this.mouseX - this.camera.position.x ) * .05;
    // this.camera.position.y += ( - this.mouseY - this.camera.position.y ) * .05;
    this.camera.lookAt( this.scene.position );
    this.renderer.render( this.scene, this.camera );
  }

  upload(event): void {
    const image = event.target.files[0];
    if (!image) { return; }
    const formData = new FormData();

    formData.append('image', image);
    this.http.post('/api/convert', formData)
      .subscribe(response => {
        this.load(image.name + '.ply');
      }, err => {
        console.log(err);
      });

  }
}
