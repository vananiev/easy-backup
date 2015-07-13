<?php
	class Vmanager{

		private $vmanager = 'sudo -u vmanager ';

		function __construct(){
			if( file_exists('/home/vmanager/vmanager/lib/vmanager') )
				$this->vmanager .= " /home/vmanager/vmanager/lib/vmanager ";
			else if( file_exists('/usr/bin/vmanager') )
				$this->vmanager .= " /usr/bin/vmanager ";
			else
				throw new Exception("Can't find vmanager utility");
		}

		/**
		* return: array
		**/
		public function vmInfo(){
			exec($this->vmanager . 'vmInfo', $stdout, $return);
			if( $return ) return array();
			unset($stdout[0]);
			asort($stdout);
			return $stdout;
		}

		/**
		* @return true or error string
		**/
		public function start( $vmName, &$stdout = null ){
			return $this->toVmanager( 'start ' . $vmName, $stdout );
		}

		/**
		* @return exit code
		* @return throw $stdout
		**/
		public function toVmanager( $command, &$stdout = null ){
			exec($this->vmanager . $command, $std_out, $return);
			if( null !== $stdout )
				$stdout = implode('\n', $std_out);
			return $return;
		}

		public function shutdown( $vmName, &$stdout = null ){
			return $this->toVmanager( 'shutdown ' . $vmName, $stdout );
		}

		public function destroy( $vmName, &$stdout = null ){
			return $this->toVmanager( 'destroy ' . $vmName, $stdout );
		}

		public function reset( $vmName, &$stdout = null ){
			return $this->toVmanager( 'reset ' . $vmName, $stdout );
		}

		public function autostartOn( $vmName, &$stdout = null ){
			return $this->toVmanager( 'autostartOn ' . $vmName, $stdout );
		}

		public function autostartOff( $vmName, &$stdout = null ){
			return $this->toVmanager( 'autostartOff ' . $vmName, $stdout );
		}

		public function backup( $vmName, &$stdout = null ){
			return $this->toVmanager( 'backup ' . $vmName, $stdout );
		}

	}
?>
